import { useState } from 'react';
import { Card, Input, Button, Spinner, Chip } from "@nextui-org/react";

export default function DiabetesPage() {
  const [formData, setFormData] = useState({
    Pregnancies: '',
    Glucose: '',
    BloodPressure: '',
    SkinThickness: '',
    Insulin: '',
    BMI: '',
    DiabetesPedigreeFunction: '',
    Age: ''
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ prediction_text: string; color: string } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/diabetes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze diabetes risk');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError('Failed to analyze diabetes risk. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="min-h-screen bg-background p-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8">Diabetes Risk Analysis</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Input Section */}
          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Enter Health Parameters</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                label="Number of Pregnancies"
                name="Pregnancies"
                type="number"
                value={formData.Pregnancies}
                onChange={handleChange}
                required
              />
              <Input
                label="Glucose Level (mg/dL)"
                name="Glucose"
                type="number"
                value={formData.Glucose}
                onChange={handleChange}
                required
              />
              <Input
                label="Blood Pressure (mm Hg)"
                name="BloodPressure"
                type="number"
                value={formData.BloodPressure}
                onChange={handleChange}
                required
              />
              <Input
                label="Skin Thickness (mm)"
                name="SkinThickness"
                type="number"
                value={formData.SkinThickness}
                onChange={handleChange}
                required
              />
              <Input
                label="Insulin Level (mu U/ml)"
                name="Insulin"
                type="number"
                value={formData.Insulin}
                onChange={handleChange}
                required
              />
              <Input
                label="BMI (kg/m²)"
                name="BMI"
                type="number"
                value={formData.BMI}
                onChange={handleChange}
                required
              />
              <Input
                label="Diabetes Pedigree Function"
                name="DiabetesPedigreeFunction"
                type="number"
                step="0.001"
                value={formData.DiabetesPedigreeFunction}
                onChange={handleChange}
                required
              />
              <Input
                label="Age"
                name="Age"
                type="number"
                value={formData.Age}
                onChange={handleChange}
                required
              />
              {error && (
                <p className="text-danger text-sm">{error}</p>
              )}
              <Button
                color="primary"
                className="w-full"
                type="submit"
                disabled={loading}
                size="lg"
              >
                {loading ? (
                  <Spinner size="sm" color="white" />
                ) : (
                  'Analyze Diabetes Risk'
                )}
              </Button>
            </form>
          </Card>

          {/* Results Section */}
          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Analysis Results</h2>
            {result ? (
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold mb-2">Prediction</h3>
                  <Chip
                    style={{ backgroundColor: result.color }}
                    className="text-white text-lg"
                    size="lg"
                  >
                    {result.prediction_text}
                  </Chip>
                </div>
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-foreground/60">
                  Enter your health parameters and click "Analyze Diabetes Risk" to get started.
                </p>
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
} 