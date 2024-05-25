const express = require('express');
const app = express();

const facedetectionRoutes = require('./routes/FaceDetect');

const cors = require('cors')
const fileUpload = require('express-fileupload');
const {cloudinaryConnect} = require('./config/cloudinary')
const dotenv = require('dotenv');
dotenv.config();

const PORT = process.env.PORT || 5000

app.use(express.json());

app.use(
    cors({
        origin: "http://localhost:3000",
        credentials: true,
    })
)

app.use(
    fileUpload({
        useTempFiles: true,
        tempFileDir: "/tmp",
    })
)

cloudinaryConnect();

app.use("/api/v1/faceDetection", facedetectionRoutes);


app.listen(PORT, () => {
    console.log('App is running')
})