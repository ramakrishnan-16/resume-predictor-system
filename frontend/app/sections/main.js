"use client";

import AppNavbar from "../components/navbar";
import { useState, useRef } from "react";
import {
  Container,
  Row,
  Col,
  Card,
  Form,
  Button,
  ProgressBar,
  Alert,
  Badge,
  Spinner
} from "react-bootstrap";
import axios from "axios";

export default function MainSection() {
  const [resume, setResume] = useState(null);
  const [score, setScore] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fileInputRef = useRef(null);

  const handleClear = () => {
    setResume(null);
    setScore(null);
    setResult(null);
    setError("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setScore(null);
    setResult(null);

    if (!resume) {
      setError("Please upload a resume file.");
      return;
    }

    const formData = new FormData();
    formData.append("resume", resume);

    try {
      setLoading(true);
      const res = await axios.post(
        "http://127.0.0.1:8000/api/predict/",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      setScore(res.data.ats_score);
      setResult(res.data);
    } catch (err) {
      setError(
        err?.response?.data?.error || "Resume analysis failed. Try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const scoreVariant =
    score >= 80
      ? "success"
      : score >= 60
      ? "info"
      : score >= 40
      ? "warning"
      : "danger";

  return (
    <Container fluid className="bg-light min-vh-100 pt-5">
      <AppNavbar onClear={handleClear} />

      <Row className="justify-content-center mt-4">
        <Col lg={8}>
          <Card className="border-0 shadow-lg rounded-4 p-4 p-md-5">
            <h2 className="fw-bold text-center mb-3">
              Resume ATS Score Predictor
            </h2>
            <p className="text-center text-muted mb-4">
              Upload your resume to check ATS friendliness & improvement tips
            </p>

            <Form onSubmit={handleSubmit}>
              <Form.Group className="mb-4">
                <Form.Label className="fw-semibold">
                  Upload Resume (PDF / DOCX)
                </Form.Label>
                <Form.Control
                  type="file"
                  accept=".pdf,.docx"
                  ref={fileInputRef}
                  onChange={(e) => setResume(e.target.files[0])}
                  className="rounded-3"
                />
              </Form.Group>

              {error && <Alert variant="danger">{error}</Alert>}

              <Button
                type="submit"
                className="w-100 py-2 fw-semibold rounded-3"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <Spinner size="sm" className="me-2" />
                    Analyzing Resume...
                  </>
                ) : (
                  "Analyze Resume"
                )}
              </Button>
            </Form>

            {score !== null && (
              <div className="mt-5">
                <div className="d-flex justify-content-between align-items-center mb-2">
                  <h5 className="mb-0">ATS Score</h5>
                  <Badge bg={scoreVariant} className="fs-6">
                    {score}/100
                  </Badge>
                </div>
                <ProgressBar
                  now={score}
                  variant={scoreVariant}
                  className="rounded-pill"
                  style={{ height: "12px" }}
                />
              </div>
            )}

            {result && (
              <div className="mt-4">
                <Alert variant={scoreVariant}>
                  <strong>Result:</strong> {result.verdict}
                </Alert>


                <Row>
                  <Col md={6}>
                    <h5 className="mb-3">⚠️ Issues Found</h5>
                    <Card className="p-3 shadow-sm rounded-3">
                      <ul className="mb-0">
                        {result.issues?.length > 0 ? (
                          result.issues.map((issue, i) => (
                            <li key={i}>{issue}</li>
                          ))
                        ) : (
                          <li>No major issues detected</li>
                        )}
                      </ul>
                    </Card>
                  </Col>

                  <Col md={6}>
                    <h5 className="mb-3">✅ Suggestions</h5>
                    <Card className="p-3 shadow-sm rounded-3">
                      <ul className="mb-0">
                        {result.suggestions?.length > 0 ? (
                          result.suggestions.map((tip, i) => (
                            <li key={i}>{tip}</li>
                          ))
                        ) : (
                          <li>Your resume is already ATS optimized</li>
                        )}
                      </ul>
                    </Card>
                  </Col>
                </Row>
              </div>
            )}
          </Card>
        </Col>
      </Row>
    </Container>
  );
}