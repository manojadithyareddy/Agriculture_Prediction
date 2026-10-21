import React from 'react';

export const DISTRICTS = [
  // Telangana
  'Hyderabad', 'Warangal', 'Hanamkonda', 'Karimnagar', 'Nizamabad', 'Khammam', 'Nalgonda',
  'Medak', 'Mahabubnagar', 'Adilabad', 'Ranga Reddy', 'Sangareddy', 'Siddipet', 'Suryapet',
  'Yadadri Bhuvanagiri', 'Jangaon', 'Jayashankar Bhupalpally', 'Jogulamba Gadwal', 'Kamareddy',
  'Komaram Bheem', 'Mahabubabad', 'Mancherial', 'Mulugu', 'Nagarkurnool', 'Narayanpet',
  'Nirmal', 'Peddapalli', 'Rajanna Sircilla', 'Vikarabad', 'Wanaparthy', 'Bhadradri Kothagudem',
  // Andhra Pradesh
  'Visakhapatnam', 'Vijayawada', 'Guntur', 'Kurnool', 'Nellore', 'Rajahmundry', 'Tirupati',
  'Kakinada', 'Kadapa', 'Anantapur', 'Eluru', 'Ongole', 'Vizianagaram', 'Machilipatnam',
  'Srikakulam', 'Chittoor', 'Nandyal', 'Bapatla', 'Palnadu', 'Konaseema', 'Anakapalli',
  'Alluri Sitharama Raju', 'Parvathipuram Manyam', 'Sri Sathya Sai', 'Annamayya', 'Krishna'
].sort();

export const CROPS = [
  'Rice', 'Maize', 'Cotton', 'Banana', 'Mango', 'Grapes', 'Orange', 'Papaya',
  'Pomegranate', 'Watermelon', 'Muskmelon', 'Coconut', 'Tender Coconut',
  'Beans', 'Blackgram', 'Chickpea', 'Pigeonpeas', 'Lentil', 'Jute', 'Coffee'
].sort();

export const GROWTH_STAGES = [
  'Initial', 'Development', 'Mid-season', 'Late-season'
];

interface SelectProps {
  value: string;
  onChange: (val: string) => void;
  id?: string;
  label?: string;
}

export function DistrictSelect({ value, onChange, id, label = 'District / Location' }: SelectProps) {
  return (
    <div className="form-group">
      <label className="form-label" htmlFor={id}>{label}</label>
      <select
        id={id}
        className="form-select"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        {DISTRICTS.map((d) => (
          <option key={d} value={d}>{d}</option>
        ))}
      </select>
    </div>
  );
}

export function CropSelect({ value, onChange, id, label = 'Crop / Commodity' }: SelectProps) {
  return (
    <div className="form-group">
      <label className="form-label" htmlFor={id}>{label}</label>
      <select
        id={id}
        className="form-select"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        {CROPS.map((c) => (
          <option key={c} value={c}>{c}</option>
        ))}
      </select>
    </div>
  );
}
