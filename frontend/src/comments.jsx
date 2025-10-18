// frontend-new/src/components/Comments.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_BASE;

export default function Comments({ taskId }) {
  const [comments, setComments] = useState([]);
  const [text, setText] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [author, setAuthor] = useState('');

  useEffect(() => {
    if (!taskId) return;
    fetchComments();
  }, [taskId]);

  // Fetch comments (GET)
  async function fetchComments() {
    try {
      const res = await axios.get(`${API_BASE}/task/${taskId}`);
      setComments(res.data);
    } catch (err) {
      console.error(err.response?.data || err.message);
      alert(`Failed to load comments: ${err.response?.data?.error || err.message}`);
    }
  }

  // Add comment (POST)
  async function addComment(e) {
    e.preventDefault();
    if (!text.trim()) return;
    try {
      const res = await axios.post(`${API_BASE}/`, { task_id: taskId, text, author });
      setComments(prev => [...prev, res.data]);
      setText('');
      setAuthor('');
    } catch (err) {
      console.error(err.response?.data || err.message);
      alert(`Add failed: ${err.response?.data?.error || err.message}`);
    }
  }

  // Update comment (PUT)
  async function updateComment(e) {
    e.preventDefault();
    if (!text.trim() || !editingId) return;
    try {
      const res = await axios.put(`${API_BASE}/${editingId}`, { text, author });
      setComments(prev => prev.map(c => (c.id === editingId ? res.data : c)));
      setText('');
      setAuthor('');
      setEditingId(null);
    } catch (err) {
      console.error(err.response?.data || err.message);
      alert(`Update failed: ${err.response?.data?.error || err.message}`);
    }
  }

  // Delete comment (DELETE)
  async function deleteComment(id) {
    if (!window.confirm('Delete comment?')) return;
    try {
      await axios.delete(`${API_BASE}/${id}`);
      setComments(prev => prev.filter(c => c.id !== id));
    } catch (err) {
      console.error(err.response?.data || err.message);
      alert(`Delete failed: ${err.response?.data?.error || err.message}`);
    }
  }

  // Start editing
  function startEdit(c) {
    setEditingId(c.id);
    setText(c.text);
    setAuthor(c.author || '');
  }

  function cancelEdit() {
    setEditingId(null);
    setText('');
    setAuthor('');
  }

  return (
    <div style={{ border: '1px solid #ddd', padding: 12 }}>
      <h3>Comments</h3>

      <form onSubmit={editingId ? updateComment : addComment}>
        <input
          placeholder="Your name (optional)"
          value={author}
          onChange={e => setAuthor(e.target.value)}
        />
        <br />
        <textarea
          placeholder="Write a comment..."
          rows={3}
          value={text}
          onChange={e => setText(e.target.value)}
          style={{ width: '100%' }}
        />
        <div style={{ marginTop: 8 }}>
          <button type="submit">{editingId ? 'Save' : 'Add comment'}</button>
          {editingId && <button type="button" onClick={cancelEdit}>Cancel</button>}
        </div>
      </form>

      <ul>
        {comments.map(c => (
          <li key={c.id} style={{ marginTop: 8 }}>
            <strong>{c.author || 'Anonymous'}</strong> · <small>{new Date(c.created_at).toLocaleString()}</small>
            <p>{c.text}</p>
            <button onClick={() => startEdit(c)}>Edit</button>
            <button onClick={() => deleteComment(c.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
