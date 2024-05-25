const express = require('express')
const router = express.Router();

const {
    faceDetection
} = require('../controllers/FaceDetection')

router.post("/detectFace", faceDetection)

module.exports = router;