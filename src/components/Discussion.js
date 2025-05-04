import { useState } from 'react';
import axios from 'axios';

export default function Discussion({ airdropId, comments, userId }) {
  const [text, setText] = useState('');
  const [inputUserId, setInputUserId] = useState(userId || '');

  const handleComment = async () => {
    if (!text || !inputUserId) return;
    await axios.post(`/api/airdrops/${airdropId}/comment`, { userId: inputUserId, text });
    setText('');
  };

  return (
    <div className="mt-4">
      <h4 className="text-lg font-semibold">Discussion</h4>
      <div className="space-y-2">
        {comments.map((comment, i) => (
          <div key={i} className="p-2 border-b">
            <p>{comment.text}</p>
            <p className="text-sm text-gray-500">Posted on {new Date(comment.createdAt).toLocaleDateString()}</p>
          </div>
        ))}
      </div>
      <div className="mt-2">
        {!userId && (
          <input
            type="text"
            value={inputUserId}
            onChange={(e) => setInputUserId(e.target.value)}
            placeholder="Enter your Telegram ID"
            className="w-full p-2 border rounded mb-2"
          />
        )}
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Add a comment..."
          className="w-full p-2 border rounded"
        />
        <button onClick={handleComment} className="mt-2 p-2 bg-blue-500 text-white rounded">
          Post Comment
        </button>
      </div>
    </div>
  );
}