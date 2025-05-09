import { useState } from 'react';
import { Button, Card, Input, Spinner, Chip, Textarea } from "@nextui-org/react";
import { analyzeSymptoms, SymptomAnalysis } from '@/services/api';

export default function IndexPage() {
  const [symptoms, setSymptoms] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState<SymptomAnalysis | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!symptoms.trim()) {
      setError('Please enter at least one symptom');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const symptomsList = symptoms.split(',').map(s => s.trim());
      const result = await analyzeSymptoms(symptomsList);
      setAnalysis(result);
    } catch (err) {
      setError('Failed to analyze symptoms. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'danger';
      case 'medium':
        return 'warning';
      case 'low':
        return 'success';
      default:
        return 'default';
    }
  };

  return (
    <div className="min-h-screen bg-background p-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8">AI Health Analysis</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Input Section */}
          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Enter Your Symptoms</h2>
            <div className="space-y-4">
              <Textarea
                label="Symptoms"
                placeholder="Enter your symptoms separated by commas (e.g., fever, cough, headache)"
                value={symptoms}
                onChange={(e) => setSymptoms(e.target.value)}
                className="w-full"
                minRows={3}
              />
              {error && (
                <p className="text-danger text-sm">{error}</p>
              )}
              <Button
                color="primary"
                className="w-full"
                onClick={handleAnalyze}
                disabled={loading}
                size="lg"
              >
                {loading ? (
                  <Spinner size="sm" color="white" />
                ) : (
                  'Analyze Symptoms'
                )}
              </Button>
            </div>
          </Card>

          {/* Results Section */}
          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Analysis Results</h2>
            {analysis ? (
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold mb-2">Severity Level</h3>
                  <Chip
                    color={getSeverityColor(analysis.severity)}
                    variant="flat"
                    size="lg"
                    className="text-lg"
                  >
                    {analysis.severity.toUpperCase()}
                  </Chip>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-2">Analysis</h3>
                  <p className="text-foreground/80 whitespace-pre-wrap">
                    {analysis.analysis}
                  </p>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-2">Recommendations</h3>
                  <ul className="list-disc list-inside space-y-2">
                    {analysis.recommendations.map((rec, index) => (
                      <li key={index} className="text-foreground/80">
                        {rec}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-foreground/60">
                  Enter your symptoms and click "Analyze Symptoms" to get started.
                </p>
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
}
