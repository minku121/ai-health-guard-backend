const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export interface SymptomAnalysis {
  symptoms: string[];
  analysis: string;
  recommendations: string[];
  severity: 'low' | 'medium' | 'high';
}

export const analyzeSymptoms = async (symptoms: string[]): Promise<SymptomAnalysis> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ symptoms }),
    });

    if (!response.ok) {
      throw new Error('Failed to analyze symptoms');
    }

    return await response.json();
  } catch (error) {
    console.error('Error analyzing symptoms:', error);
    throw error;
  }
}; 