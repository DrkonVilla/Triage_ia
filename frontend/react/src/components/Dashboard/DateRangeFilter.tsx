import { useState } from 'react';
import { DateRangePicker } from 'react-date-range';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';
import { Calendar } from 'lucide-react';
import 'react-date-range/dist/styles.css';
import 'react-date-range/dist/theme/default.css';

interface DateRangeFilterProps {
  startDate: Date;
  endDate: Date;
  onRangeChange: (start: Date, end: Date) => void;
}

export const DateRangeFilter: React.FC<DateRangeFilterProps> = ({
  startDate,
  endDate,
  onRangeChange
}) => {
  const [showPicker, setShowPicker] = useState(false);
  const [selection, setSelection] = useState({
    startDate,
    endDate,
    key: 'selection'
  });
  
  const handleSelect = (ranges: any) => {
    const { startDate, endDate } = ranges.selection;
    setSelection(ranges.selection);
    onRangeChange(startDate, endDate);
    setShowPicker(false);
  };
  
  return (
    <div className="relative">
      <button
        onClick={() => setShowPicker(!showPicker)}
        className="flex items-center space-x-2 px-4 py-2 bg-white border rounded-lg shadow-sm hover:bg-gray-50"
      >
        <Calendar className="h-4 w-4 text-gray-500" />
        <span className="text-sm">
          {format(startDate, 'dd/MM/yyyy', { locale: es })} - {format(endDate, 'dd/MM/yyyy', { locale: es })}
        </span>
      </button>
      
      {showPicker && (
        <div className="absolute top-full mt-2 z-10 shadow-lg">
          <DateRangePicker
            ranges={[selection]}
            onChange={handleSelect}
            moveRangeOnFirstSelection={false}
            locale={es}
            months={2}
            direction="horizontal"
          />
        </div>
      )}
    </div>
  );
};