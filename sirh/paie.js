const express = require('express');
const fileUpload = require('express-fileupload');
const { exec } = require('child_process');
const app = express();
const PORT = 3000;

// Serveur de fichiers statiques
app.use('/pages', express.static('pages')); // Remplacez par le chemin réel

app.use(fileUpload());
app.use(express.static('public'));

app.post('/api/upload-pdf', (req, res) => {
    let uploadedFile = req.files.pdf;
    const filePath = __dirname + '/uploads/' + uploadedFile.name;
    
    uploadedFile.mv(filePath, async (err) => {
        if (err) {
            return res.status(500).send(err);
        }

        exec(`python3 extract_payroll_info.py ${filePath}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error executing Python script: ${error}`);
                return res.status(500).json({ error: 'Internal Server Error' });
            }
            
            if (stderr) {
                console.error(`Python Script Error: ${stderr}`);
                return res.status(500).json({ error: 'Internal Server Error' });
            }
            
            const results = JSON.parse(stdout);
            res.json(results);
        });
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
