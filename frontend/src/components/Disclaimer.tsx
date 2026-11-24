import React from 'react';

interface DisclaimerProps {
  customText?: string;
}

export const Disclaimer: React.FC<DisclaimerProps> = ({ customText }) => {
  return (
    <div className="p-3 bg-slate-50 border border-[#E3E8E5] rounded text-[11px] text-[#586563] leading-relaxed">
      <strong className="text-[#202A2A]">Medical Notice:</strong>{' '}
      {customText ||
        "OncoSathi provides educational simplifications grounded in verified sources. It does not replace certified physician evaluation, clinical diagnosis, or prescriptions."}
    </div>
  );
};
