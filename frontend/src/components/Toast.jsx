export default function Toast({ message, type = 'success' }) {
  if (!message) return null;
  return <div className={`toast-note ${type}`}>{message}</div>;
}
