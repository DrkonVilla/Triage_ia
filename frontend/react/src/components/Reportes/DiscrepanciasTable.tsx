import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from '@tanstack/react-table';
import type { Discrepancia } from '../../types';

const columnHelper = createColumnHelper<Discrepancia>();

const columns = [
  columnHelper.accessor('fecha', {
    header: 'Fecha',
    cell: (info) => new Date(info.getValue()).toLocaleDateString('es-CL'),
  }),
  columnHelper.accessor('paciente', {
    header: 'Paciente',
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor('nivel_ia', {
    header: 'Nivel IA',
    cell: (info) => {
      const value = info.getValue();
      const colors: Record<string, string> = {
        RED: 'bg-red-100 text-red-800',
        ORANGE: 'bg-orange-100 text-orange-800',
        YELLOW: 'bg-yellow-100 text-yellow-800',
        GREEN: 'bg-green-100 text-green-800',
        BLUE: 'bg-blue-100 text-blue-800',
      };
      return (
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[value]}`}>
          {value}
        </span>
      );
    },
  }),
  columnHelper.accessor('nivel_humano', {
    header: 'Nivel Enfermera',
    cell: (info) => {
      const value = info.getValue();
      const colors: Record<string, string> = {
        RED: 'bg-red-100 text-red-800',
        ORANGE: 'bg-orange-100 text-orange-800',
        YELLOW: 'bg-yellow-100 text-yellow-800',
        GREEN: 'bg-green-100 text-green-800',
        BLUE: 'bg-blue-100 text-blue-800',
      };
      return (
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[value]}`}>
          {value}
        </span>
      );
    },
  }),
  columnHelper.accessor('diferencia', {
    header: 'Diferencia',
    cell: (info) => {
      const value = info.getValue();
      return (
        <span className="text-gray-600">
          {value} niveles
        </span>
      );
    },
  }),
  columnHelper.accessor('tipo', {
    header: 'Tipo',
    cell: (info) => {
      const value = info.getValue();
      const isMajor = value.includes('Sobre') || value.includes('Sub');
      return (
        <span className={isMajor ? 'text-red-600 font-semibold' : 'text-yellow-600'}>
          {value}
        </span>
      );
    },
  }),
];

interface DiscrepanciasTableProps {
  data: Discrepancia[];
}

export const DiscrepanciasTable: React.FC<DiscrepanciasTableProps> = ({ data }) => {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });
  
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th
                  key={header.id}
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {flexRender(header.column.columnDef.header, header.getContext())}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id} className="hover:bg-gray-50">
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id} className="px-6 py-4 whitespace-nowrap text-sm">
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      
      {data.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No hay discrepancias registradas en el período seleccionado
        </div>
      )}
    </div>
  );
};