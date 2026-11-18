import fs from 'fs';
import path from 'path';
import { defineConfig } from 'vite';

function serveStaticSubpages() {
  const middleware = (req, res, next) => {
    const rawUrl = (req.url || '').split('?')[0];
    if (!rawUrl || rawUrl === '/' || rawUrl.includes('.')) {
      return next();
    }
    const cleanPath = rawUrl.replace(/^\/+|\/+$/g, '');
    const candidate = path.resolve(process.cwd(), 'public', cleanPath, 'index.html');
    if (fs.existsSync(candidate)) {
      res.statusCode = 200;
      res.setHeader('Content-Type', 'text/html; charset=utf-8');
      res.end(fs.readFileSync(candidate, 'utf-8'));
      return;
    }
    next();
  };

  return {
    name: 'bugwrite-static-subpages',
    configureServer(server) {
      server.middlewares.use(middleware);
    },
    configurePreviewServer(server) {
      server.middlewares.use(middleware);
    },
  };
}

export default defineConfig({
  plugins: [serveStaticSubpages()],
});
