import { useEffect, useState } from 'react';

export interface SheetData {
  [key: string]: string | number;
}

export interface SheetInfo {
  name: string;
  gid: string;
  data: SheetData[];
}

const SHEET_ID = '1vkBUlqKyquL6auioTkW_kNMvLqpRohgyCfHvV0viR58';

/**
 * Hook para buscar dados do Google Sheets automaticamente
 * Detecta novas abas e carrega dados em tempo real
 * Usa CSV export para melhor compatibilidade com CORS
 */
export function useGoogleSheets() {
  const [sheets, setSheets] = useState<SheetInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSheets = async () => {
      try {
        setLoading(true);
        setError(null);

        // Lista de abas conhecidas (será expandida conforme novas abas forem adicionadas)
        // Para agora, vamos usar os GIDs conhecidos
        const knownSheets = [
          { name: 'Chamados Janeiro', gid: 1963619439 },
          { name: 'Chamados Fevereiro', gid: 0 }, // Será descoberto dinamicamente
        ];

        const sheetsData: SheetInfo[] = [];

        // Tentar buscar dados de cada aba conhecida
        for (const sheet of knownSheets) {
          try {
            // Usar CSV export para melhor compatibilidade
            const csvUrl = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/export?format=csv&gid=${sheet.gid}`;
            
            const csvResponse = await fetch(csvUrl, {
              method: 'GET',
              headers: {
                'Accept': 'text/csv',
              },
            });

            if (!csvResponse.ok) {
              console.warn(`Aba ${sheet.name} nao encontrada (GID: ${sheet.gid})`);
              continue;
            }

            const csv = await csvResponse.text();
            
            if (!csv || csv.trim().length === 0) {
              console.warn(`Aba ${sheet.name} vazia`);
              continue;
            }

            const lines = csv.trim().split('\n');

            if (lines.length < 2) {
              console.warn(`Aba ${sheet.name} sem dados`);
              continue;
            }

            // Parse CSV
            const headers = parseCSVLine(lines[0]);
            const data: SheetData[] = [];

            for (let i = 1; i < lines.length; i++) {
              const values = parseCSVLine(lines[i]);
              
              // Pular linhas vazias
              if (values.every(v => !v || v.trim() === '')) {
                continue;
              }

              const row: SheetData = {};

              headers.forEach((header, index) => {
                row[header] = values[index] || '';
              });

              data.push(row);
            }

            if (data.length > 0) {
              sheetsData.push({
                name: sheet.name,
                gid: String(sheet.gid),
                data,
              });
            }
          } catch (err) {
            console.error(`Erro ao processar aba ${sheet.name}:`, err);
          }
        }

        if (sheetsData.length === 0) {
          setError('Nenhuma aba de chamados encontrada na planilha');
        } else {
          setSheets(sheetsData);
        }
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Erro desconhecido ao buscar planilha';
        setError(message);
        console.error('Erro ao buscar sheets:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchSheets();

    // Recarregar dados a cada 5 minutos
    const interval = setInterval(fetchSheets, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  return { sheets, loading, error };
}

/**
 * Parse CSV line respeitando aspas
 */
function parseCSVLine(line: string): string[] {
  const result: string[] = [];
  let current = '';
  let insideQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    const nextChar = line[i + 1];

    if (char === '"') {
      if (insideQuotes && nextChar === '"') {
        current += '"';
        i++; // Skip next quote
      } else {
        insideQuotes = !insideQuotes;
      }
    } else if (char === ',' && !insideQuotes) {
      result.push(current.trim());
      current = '';
    } else {
      current += char;
    }
  }

  result.push(current.trim());
  return result;
}

/**
 * Agregar dados por periodo
 */
export function aggregateByMonth(sheets: SheetInfo[]) {
  const aggregated: { [month: string]: SheetData[] } = {};

  sheets.forEach((sheet) => {
    aggregated[sheet.name] = sheet.data;
  });

  return aggregated;
}

/**
 * Calcular estatisticas gerais
 */
export function calculateStats(sheets: SheetInfo[]) {
  const stats = {
    totalChamados: 0,
    totalMeses: sheets.length,
    porPonto: {} as { [key: string]: number },
    porCidade: {} as { [key: string]: number },
    porTipoFalha: {} as { [key: string]: number },
    porAmbiente: {} as { [key: string]: number },
  };

  sheets.forEach((sheet) => {
    sheet.data.forEach((row) => {
      stats.totalChamados++;

      const ponto = String(row['Ponto'] || 'N/A');
      const cidade = String(row['Cidade'] || 'N/A');
      const tipoFalha = String(row['Tipo de Falha'] || 'N/A');
      const ambiente = String(row['Ambiente'] || 'N/A');

      stats.porPonto[ponto] = (stats.porPonto[ponto] || 0) + 1;
      stats.porCidade[cidade] = (stats.porCidade[cidade] || 0) + 1;
      stats.porTipoFalha[tipoFalha] = (stats.porTipoFalha[tipoFalha] || 0) + 1;
      stats.porAmbiente[ambiente] = (stats.porAmbiente[ambiente] || 0) + 1;
    });
  });

  return stats;
}
