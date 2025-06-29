import fs from 'fs';
import path from 'path';

export default async function handler(req, res) {
  // Configurar CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Manejar preflight requests
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Solo permitir POST
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  try {
    const statsData = req.body;
    
    // En Vercel, no podemos escribir archivos directamente
    // Por ahora, solo loggeamos los datos
    console.log('Stats data received:', JSON.stringify(statsData, null, 2));
    
    // Responder con éxito
    res.status(200).json({ 
      status: 'success',
      message: 'Stats logged (file writing not available in Vercel)'
    });
    
  } catch (error) {
    console.error('Error saving stats:', error);
    res.status(500).json({ error: error.message });
  }
} 