const express = require('express')
const fs = require('fs')
const app = express()
const port = 3000

// app.get('/video', function (req, res) {
//     const path = '../results/2019-11-07/1573120505.9512043.avi'
//     console.log('\n\nserving video from ' + path)
//     const stat = fs.statSync(path)
//     const fileSize = stat.size

//     const head = {
//         'Content-Length': fileSize,
//         'Content-Type': 'video/mp4',
//     }

//     res.writeHead(200, head)
//     fs.createReadStream(path).pipe(res)
// });

app.get('/video', function (req, res) {
    const path = '.' + req.query.path
    console.log('\n\n\n' + path)
    fs.stat(path, (err, stat) => {

        // Handle file not found
        if (err !== null && err.code === 'ENOENT') {
            res.sendStatus(404);
        }

        const fileSize = stat.size
        const range = req.headers.range

        if (range) {

            const parts = range.replace(/bytes=/, "").split("-");

            const start = parseInt(parts[0], 10);
            const end = parts[1] ? parseInt(parts[1], 10) : fileSize - 1;

            const chunksize = (end - start) + 1;
            const file = fs.createReadStream(path, {
                start,
                end
            });
            const head = {
                'Content-Range': `bytes ${start}-${end}/${fileSize}`,
                'Accept-Ranges': 'bytes',
                'Content-Length': chunksize,
                'Content-Type': 'video/mp4',
            }

            res.writeHead(206, head);
            file.pipe(res);
        } else {
            const head = {
                'Content-Length': fileSize,
                'Content-Type': 'video/mp4',
            }

            res.writeHead(200, head);
            fs.createReadStream(path).pipe(res);
        }
    });
});

app.listen(port, () => console.log(`Node server listening on port ${port}!`))