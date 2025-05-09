import { useState } from 'react';
import { Card, Input, Button, Spinner, Chip, Select, SelectItem } from "@nextui-org/react";

export default function HeartPage() {
  const [formData, setFormData] = useState({
    age: '',
    sex: '',
    cp: '',
    trestbps: '',
    chol: '',
    fbs: '',
    restecg: '',
    thalach: '',
    exang: '',
    oldpeak: '',
    slope: '',
    ca: '',
    thal: ''
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ prediction_text: string; color: string } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/heart', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze heart condition');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError('Failed to analyze heart condition. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="min-h-screen bg-background p-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8">Heart Disease Analysis</h1>
        
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
              <Select
                label="Sex"
                name="sex"
                value={formData.sex}
                onChange={handleChange}
                required
              >
                <SelectItem key="Male" value="Male">Male</SelectItem>
                <SelectItem key="Female" value="Female">Female</SelectItem>
              </Select>
              <Select
                label="Chest Pain Type"
                name="cp"
                value={formData.cp}
                onChange={handleChange}
                required
              >
                <SelectItem key="Low pain" value="Low pain">Low pain</SelectItem>
                <SelectItem key="Mild pain" value="Mild pain">Mild pain</SelectItem>
                <SelectItem key="Moderate pain" value="Moderate pain">Moderate pain</SelectItem>
                <SelectItem key="Extreme pain" value="Extreme pain">Extreme pain</SelectItem>
              </Select>
              <Input
                label="Resting Blood Pressure"
                name="trestbps"
                type="number"
                value={formData.trestbps}
                onChange={handleChange}
                required
              />
              <Input
                label="Cholesterol"
                name="chol"
                type="number"
                value={formData.chol}
                onChange={handleChange}
                required
              />
              <Select
                label="Fasting Blood Sugar > 120 mg/dl"
                name="fbs"
                value={formData.fbs}
                onChange={handleChange}
                required
              >
                <SelectItem key="Yes" value="Yes">Yes</SelectItem>
                <SelectItem key="No" value="No">No</SelectItem>
              </Select>
              <Input
                label="Resting ECG Results"
                name="restecg"
                type="number"
                value={formData.restecg}
                onChange={handleChange}
                required
              />
              <Input
                label="Maximum Heart Rate"
                name="thalach"
                type="number"
                value={formData.thalach}
                onChange={handleChange}
                required
              />
              <Select
                label="Exercise Induced Angina"
                name="exang"
                value={formData.exang}
                onChange={handleChange}
                required
              >
                <SelectItem key="Yes" value="Yes">Yes</SelectItem>
                <SelectItem key="No" value="No">No</SelectItem>
              </Select>
              <Input
                label="ST Depression"
                name="oldpeak"
                type="number"
                value={formData.oldpeak}
                onChange={handleChange}
                required
              />
              <Input
                label="Slope of Peak Exercise ST"
                name="slope"
                type="number"
                value={formData.slope}
                onChange={handleChange}
                required
              />
              <Input
                label="Number of Major Vessels"
                name="ca"
                type="number"
                value={formData.ca}
                onChange={handleChange}
                required
              />
              <Select
                label="Thalassemia"
                name="thal"
                value={formData.thal}
                onChange={handleChange}
                required
              >
                <SelectItem key="Normal" value="Normal (No Thalassemia)">Normal (No Thalassemia)</SelectItem>
                <SelectItem key="Fixed Defect" value="Fixed Defect (Beta-thalassemia minor)">Fixed Defect (Beta-thalassemia minor)</SelectItem>
                <SelectItem key="Reversible Defect" value="Reversible Defect (Beta-thalassemia intermedia)">Reversible Defect (Beta-thalassemia intermedia)</SelectItem>
                <SelectItem key="Serious Defect" value="Serious Defect (Beta-thalassemia major)">Serious Defect (Beta-thalassemia major)</SelectItem>
              </Select>
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
                  'Analyze Heart Condition'
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
                  Enter your health parameters and click "Analyze Heart Condition" to get started.
                </p>
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
} 