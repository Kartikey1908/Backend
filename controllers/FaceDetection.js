const {spawn} = require('child_process');
const { uploadImageToCloudinary } = require('../utils/imageUploader');
require('dotenv').config();

const onScriptClose = async(code, req, res, fileToBeUploaded) => {
    console.log(`Child process close all stdio with code ${code}`);
    try {
        const uploadedImage = await uploadImageToCloudinary(fileToBeUploaded, process.env.FOLDER_NAME)

        return res.status(200).json({
            success: true, 
            message: "Request reached here",
            image: uploadedImage.secure_url
        })

    }  catch (error) {
        console.log("Error occured while uploading image to cloudinary", error);
        return res.status(500).json({
            success: false,
            message: "Error occured while uploding file to clodinary",
            error : error.message,
        })
    }

    
}

exports.faceDetection = async(req, res) => {

    try {
        const {imageFile} = req.files

        if (!imageFile) {
            return res.status(404).json({
                success: false,
                message: "Image file need to be sent",
            });
        }

        var fileToBeUploaded;
        const python = await spawn('python', ['./python_scripts/faceDetection.py', imageFile.tempFilePath]);

        python.stdout.on('data', function (data) {
            console.log('Pipe data from python script...');
            fileToBeUploaded = data.toString();
            console.log(fileToBeUploaded.trim())
        })


        return python.on('close', (code) => onScriptClose(code, req, res, fileToBeUploaded.trim()));
    } catch (error) {
        console.log("Error occured", error);
        return res.status(500).json({
            success: false,
            message: "Internal Server Error",
            error: error
        })
    }
}