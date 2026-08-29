const fs = require('fs');
const file = 'backend/src/controllers/aiController.ts';
let code = fs.readFileSync(file, 'utf8');

// We will change:
// if (error && error.status) {
//    return res.status(error.status).json({ error: error.message });
// }
// To:
// if (error && error.status) {
//    const statusCode = (error.status === 404 || error.status === 403) ? 500 : error.status;
//    return res.status(statusCode).json({ error: error.message });
// }

code = code.replace(
  /if \(error && error\.status\) \{\s*return res\.status\(error\.status\)\.json\(\{ error: error\.message \}\);\s*\}/g,
  `if (error && error.status) {\n      const statusCode = (error.status === 404 || error.status === 403) ? 500 : error.status;\n      return res.status(statusCode).json({ error: error.message });\n    }`
);

fs.writeFileSync(file, code);
