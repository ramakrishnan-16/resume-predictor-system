"use client";

import { Navbar, Container, Button } from "react-bootstrap";

export default function AppNavbar({ onClear }) {
  return (
    <Navbar
      bg="white"
      className="shadow-sm px-4"
      fixed="top"
    >
      <Container fluid>
        <Navbar.Brand className="fw-bold fs-5">
          Resume Predictor System
        </Navbar.Brand>

        <Button
          variant="outline-danger"
          className="fw-semibold rounded-pill"
          onClick={onClear}
        >
          Clear
        </Button>
      </Container>
    </Navbar>
  );
}