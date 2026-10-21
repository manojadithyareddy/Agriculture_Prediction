'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';

export interface FarmContextType {
  farmId: string;
  farmName: string;
  parcelId: string;
  crop: string;
  season: string;
  location: string;
  district: string;
  state: string;
  lastSynced: string;
  systemStatus: 'Operational' | 'Degraded' | 'Offline';
  isSimulationMode: boolean;
  setSimulationMode: (enabled: boolean) => void;
  setFarmId: (id: string) => void;
  setParcelId: (parcel: string) => void;
  setCrop: (crop: string) => void;
  setDistrict: (district: string) => void;
  triggerSync: () => void;
}

export const FARMS = [
  { id: 'HYD-TEL-2026-04', name: 'Telangana Agritech Cluster Alpha', district: 'Hyderabad', state: 'Telangana', parcels: ['A1', 'A2', 'A3', 'A4', 'B1', 'B2'], defaultCrop: 'Cotton' },
  { id: 'WGL-TEL-2026-02', name: 'Warangal Precision Farm North', district: 'Warangal', state: 'Telangana', parcels: ['N1', 'N2', 'N3', 'S1'], defaultCrop: 'Rice' },
  { id: 'GNT-AP-2026-08', name: 'Guntur High-Density Commercial Plot', district: 'Guntur', state: 'Andhra Pradesh', parcels: ['G1', 'G2', 'G3'], defaultCrop: 'Chilli' },
  { id: 'KRN-AP-2026-11', name: 'Kurnool Semi-Arid Pilot Zone', district: 'Kurnool', state: 'Andhra Pradesh', parcels: ['K1', 'K2'], defaultCrop: 'Maize' },
];

const GlobalContext = createContext<FarmContextType | undefined>(undefined);

export function GlobalContextProvider({ children }: { children: React.ReactNode }) {
  const [farmId, setFarmIdState] = useState<string>('HYD-TEL-2026-04');
  const [parcelId, setParcelId] = useState<string>('A4');
  const [crop, setCrop] = useState<string>('Cotton');
  const [district, setDistrictState] = useState<string>('Hyderabad');
  const [state, setState] = useState<string>('Telangana');
  const [lastSynced, setLastSynced] = useState<string>('Just now');
  const [systemStatus] = useState<'Operational' | 'Degraded' | 'Offline'>('Operational');
  const [isSimulationMode, setSimulationModeState] = useState<boolean>(false);

  const currentFarm = FARMS.find((f) => f.id === farmId) || FARMS[0];

  useEffect(() => {
    const savedDistrict = localStorage.getItem('agrifusion_location') || 'Hyderabad';
    const foundFarm = FARMS.find((f) => f.district.toLowerCase() === savedDistrict.toLowerCase());
    if (foundFarm) {
      setFarmIdState(foundFarm.id);
      setDistrictState(foundFarm.district);
      setState(foundFarm.state);
      setCrop(foundFarm.defaultCrop);
    }

    const savedSim = localStorage.getItem('agrifusion_simulation_mode');
    if (savedSim === 'true') {
      setSimulationModeState(true);
    }
  }, []);

  const setSimulationMode = (enabled: boolean) => {
    setSimulationModeState(enabled);
    localStorage.setItem('agrifusion_simulation_mode', enabled ? 'true' : 'false');
  };

  const setFarmId = (id: string) => {
    const target = FARMS.find((f) => f.id === id);
    if (target) {
      setFarmIdState(target.id);
      setDistrictState(target.district);
      setState(target.state);
      setCrop(target.defaultCrop);
      setParcelId(target.parcels[0] || 'A1');
      localStorage.setItem('agrifusion_location', target.district);
      window.dispatchEvent(new CustomEvent('agrifusion:location-change', { detail: target.district }));
      setLastSynced('Just now');
    }
  };

  const setDistrict = (dist: string) => {
    setDistrictState(dist);
    localStorage.setItem('agrifusion_location', dist);
    const matchedFarm = FARMS.find((f) => f.district.toLowerCase() === dist.toLowerCase());
    if (matchedFarm) {
      setFarmIdState(matchedFarm.id);
      setState(matchedFarm.state);
    }
    window.dispatchEvent(new CustomEvent('agrifusion:location-change', { detail: dist }));
    setLastSynced('Just now');
  };

  const triggerSync = () => {
    setLastSynced('Just now');
  };

  return (
    <GlobalContext.Provider
      value={{
        farmId,
        farmName: currentFarm.name,
        parcelId,
        crop,
        season: 'Kharif 2026',
        location: `${district}, ${state}`,
        district,
        state,
        lastSynced,
        systemStatus,
        isSimulationMode,
        setSimulationMode,
        setFarmId,
        setParcelId,
        setCrop,
        setDistrict,
        triggerSync,
      }}
    >
      {children}
    </GlobalContext.Provider>
  );
}

export function useGlobalContext(): FarmContextType {
  const context = useContext(GlobalContext);
  if (!context) {
    throw new Error('useGlobalContext must be used within a GlobalContextProvider');
  }
  return context;
}
