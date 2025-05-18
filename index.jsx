import React from 'react';
import OrgMappingForm from '../components/OrgMappingForm';

export default function Home() {
  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold mb-4">Organizational Mapping Tool</h1>
      <OrgMappingForm />
    </main>
  );
}
