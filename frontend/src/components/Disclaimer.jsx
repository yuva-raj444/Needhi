import React from 'react';
import { DISCLAIMER } from '../utils/constants';

export default function Disclaimer({ language }) {
  const textTa =
    '⚠️ இந்த AI பொதுவான சட்ட தகவல்களை வழங்குகிறது, இது தொழில்முறை சட்ட ஆலோசனைக்கு மாற்றாக இல்லை. குறிப்பிட்ட சட்ட விஷயங்களுக்கு தகுதியான வழக்கறிஞரை அணுகவும்.';

  return (
    <div className="disclaimer-bar">
      {language === 'ta' ? textTa : DISCLAIMER}
    </div>
  );
}
