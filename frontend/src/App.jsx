import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const formatARS = (value) =>
  new Intl.NumberFormat("es-AR", {
    style: "currency",
    currency: "ARS",
    maximumFractionDigits: 2,
  }).format(value);

function App() {
  const [horas, setHoras] = useState(40);
  const [antiguedad, setAntiguedad] = useState(2);
  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState(null);
  const [cargando, setCargando] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setCargando(true);
    setError(null);
    setResultado(null);

    try {
      const response = await fetch(`${API_URL}/api/liquidacion`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          horas_trabajadas: Number(horas),
          antiguedad: Number(antiguedad),
        }),
      });

      if (!response.ok) {
        const detail = await response.json().catch(() => null);
        throw new Error(
          detail?.detail
            ? Array.isArray(detail.detail)
              ? detail.detail.map((d) => d.msg).join(", ")
              : detail.detail
            : "No se pudo calcular la liquidación."
        );
      }

      const data = await response.json();
      setResultado(data);
    } catch (err) {
      setError(err.message || "Ocurrió un error al conectar con la API.");
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="page">
      <header className="masthead">
        <span className="masthead__mark">LIQ-01</span>
        <h1 className="masthead__title">Liquidación de Sueldos</h1>
        <p className="masthead__subtitle">
          Demo de CI/CD &mdash; FastAPI + React &middot; Render + Netlify - Adrian Jose Maria Ibañez
        </p>
      </header>

      <main className="receipt">
        <section className="receipt__panel receipt__panel--form">
          <h2 className="panel-label">Datos del empleado</h2>
          <form onSubmit={handleSubmit} className="form">
            <label className="field">
              <span className="field__label">Horas trabajadas</span>
              <input
                type="number"
                min="0"
                value={horas}
                onChange={(e) => setHoras(e.target.value)}
                required
              />
            </label>

            <label className="field">
              <span className="field__label">Antigüedad (años)</span>
              <input
                type="number"
                min="0"
                value={antiguedad}
                onChange={(e) => setAntiguedad(e.target.value)}
                required
              />
            </label>

            <button type="submit" className="btn" disabled={cargando}>
              {cargando ? "Calculando…" : "Calcular liquidación"}
            </button>

            {error && <p className="error" role="alert">⚠ {error}</p>}
          </form>
        </section>

        <section className="receipt__panel receipt__panel--result">
          <h2 className="panel-label">Comprobante</h2>

          {!resultado && !error && (
            <p className="empty-state">
              Completá los datos y calculá para ver el desglose acá.
            </p>
          )}

          {resultado && (
            <div className="ticket">
              <div className="ticket__row">
                <span>Horas trabajadas</span>
                <span>{resultado.horas_trabajadas} hs</span>
              </div>
              <div className="ticket__row">
                <span>Antigüedad</span>
                <span>{resultado.antiguedad} años</span>
              </div>
              <div className="ticket__divider" />
              <div className="ticket__row">
                <span>Sueldo básico</span>
                <span>{formatARS(resultado.sueldo_basico)}</span>
              </div>
              <div className="ticket__row">
                <span>Sueldo bruto</span>
                <span>{formatARS(resultado.sueldo_bruto)}</span>
              </div>
              <div className="ticket__divider" />
              <div className="ticket__row ticket__row--total">
                <span>Sueldo neto</span>
                <span>{formatARS(resultado.sueldo_neto)}</span>
              </div>
            </div>
          )}
        </section>
      </main>

      <footer className="footnote">
        API: <code>{API_URL}</code>
      </footer>
    </div>
  );
}

export default App;
