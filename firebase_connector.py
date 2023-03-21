import uuid
import cv2


class StorageConnector:
    def __init__(self, bucket):
        self.bucket = bucket

    def upload(self, localPath, imagePath):
        imageBlob = self.bucket.blob(imagePath)
        imageBlob.upload_from_filename(localPath)

    def download(self, imagePath, localPath):
        imageBlob = self.bucket.blob(imagePath)
        imageBlob.download_to_filename(localPath)

    def rotate(self, imagePath):
        imageBlob = self.bucket.blob(imagePath)
        tmpFilePath = f"tmp/{str(uuid.uuid4())}.jpg"
        imageBlob.download_to_filename(tmpFilePath)

        img = cv2.imread(tmpFilePath)
        rotatedImg = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        cv2.imwrite(tmpFilePath, rotatedImg)

        self.upload(tmpFilePath, imagePath)
        
    def compress(self, imagePath):
        imageBlob = self.bucket.blob(imagePath)
        tmpFilePath = f"tmp/{str(uuid.uuid4())}.jpg"
        imageBlob.download_to_filename(tmpFilePath)

        img = cv2.imread(tmpFilePath)
        compressedImg = cv2.resize(img, (200, 200), interpolation = cv2.INTER_AREA)
        cv2.imwrite(tmpFilePath, compressedImg)

        self.upload(tmpFilePath, imagePath)

    def delete(self, imagePath):
        imageBlob = self.bucket.blob(imagePath)
        imageBlob.delete()
