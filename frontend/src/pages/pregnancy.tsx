import { useState } from 'react';
import { Card, Input, Button, Spinner, Chip } from "@nextui-org/react";

export default function PregnancyPage() {
  const [formData, setFormData] = useState({
    age: '',
    diastolicBP: '',
    BS: '',
    bodyTemp: '',
    heartRate: ''
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ risk_level: string; color: string } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/pregnancy', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze pregnancy risk');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError('Failed to analyze pregnancy risk. Please try again.');
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
        <h1 className="text-3xl font-bold text-center mb-8">Pregnancy Risk Analysis</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Input Section */}
          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Enter Health Parameters</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                label="Age"
                name="age"
                type="number"
                value={formData.age}
                onChange={handleChange}
                required
              />
              <Input
                label="Diastolic Blood Pressure"
                name="diastolicBP"
                type="number"
                value={formData.diastolicBP}
                onChange={handleChange}
                required
              />
              <Input
                label="Blood Sugar (BS)"
                name="BS"
                type="number"
                value={formData.BS}
                onChange={handleChange}
                required
              />
              <Input
                label="Body Temperature"
                name="bodyTemp"
                type="number"
                value={formData.bodyTemp}
                onChange={handleChange}
                required
              />
              <Input
                label="Heart Rate"
                name="heartRate"
                type="number"
                value={formData.heartRate}
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
                  'Analyze Risk'
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
                  <h3 className="text-lg font-semibold mb-2">Risk Level</h3>
                  <Chip
                    style={{ backgroundColor: result.color }}
                    className="text-white text-lg"
                    size="lg"
                  >
                    {result.risk_level}
                  </Chip>
                </div>
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-foreground/60">
                  Enter your health parameters and click "Analyze Risk" to get started.
                </p>
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
} 