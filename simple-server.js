import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

// Minimal auth endpoint to avoid spinner when unauthenticated
app.get('/api/auth/user', (_req, res) => {
	res.status(401).json({ error: 'unauthenticated' });
});

// Redirect API calls to backend on port 5000 (preserves method/body)
app.use('/api', (req, res) => {
	const target = `http://localhost:5000${req.originalUrl}`;
	res.redirect(307, target);
});

// Serve prebuilt static files from dist/public
const staticRoot = path.join(__dirname, 'dist', 'public');
app.use(express.static(staticRoot));

// SPA fallback to index.html
app.get('*', (_req, res) => {
	res.sendFile(path.join(staticRoot, 'index.html'));
});

const port = process.env.PORT ? Number(process.env.PORT) : 3000;
app.listen(port, () => {
	console.log(`✅ Frontend served at http://localhost:${port}`);
});
