# data that should go to `.json` files of webdataset
WDS_TAR_SHARDS = [
    {
        "uid": "d142ae70686e14ccc379c01a571501b5",
        "face_bboxes": [],
        "caption": "Customizing Windows 7 Setup Please Help Solved",
        "url": "https://i.imgur.com/mXQrfNs.png",
        "key": "000000000000",
        "status": "success",
        "error_message": "",
        "width": 512,
        "height": 270,
        "original_width": 1704,
        "original_height": 899,
        "exif": "{}",
        "sha256": "4052f3d8b1f5acee73e234ac8e7c614c5a6e10312d21a65d77b3ffad4edd6b31",
    },
    {
        "uid": "99e71895357f06965a6c5b00d506e5aa",
        "face_bboxes": [
            [
                0.5005972981452942,
                0.13604149222373962,
                0.8109994530677795,
                0.7247588038444519,
            ]
        ],
        "caption": "Jack Strong Official Trailer 1 (2015)   Patrick Wilson Drama Thriller HD",
        "url": "http://i.ytimg.com/vi/if2V1iszwuA/default.jpg",
        "key": "000000000001",
        "status": "success",
        "error_message": "",
        "width": 120,
        "height": 90,
        "original_width": 120,
        "original_height": 90,
        "exif": "{}",
        "sha256": "9619f8da8b04628994741ed7626d88ace59962824aff43407fee95da488d0ca7",
    },
    {
        "uid": "abff9068a3bf22d8325b61a9b1404009",
        "face_bboxes": [],
        "caption": "mercedes jeep 2015 mercedes jeep 2015 mercedes g63 amg best images collections",
        "url": "http://t0.gstatic.com/images?q=tbn:ANd9GcScIHR33LnMpupkxbZRqnj1YMvOXsc9uUTj8Wa2v8bhSjWTxTRo1w",
        "key": "000000000002",
        "status": "success",
        "error_message": "",
        "width": 275,
        "height": 183,
        "original_width": 275,
        "original_height": 183,
        "exif": "{}",
        "sha256": "042442926251b1d05345715ea91fb3b2f77b37b2c43af37cbf32cab54a0e6b1a",
    },
    {
        "uid": "7fa8b7f6ececc9dc80434f3cb6897c27",
        "face_bboxes": [],
        "caption": "WEN Fall Ginger Pumpkin Cleansing Conditioner ~ 16 oz ~  sealed  plus 6 oz Mist",
        "url": "http://thumbs.ebaystatic.com/images/g/5kAAAOSwc1FXcDFI/s-l225.jpg",
        "key": "000000000003",
        "status": "success",
        "error_message": "",
        "width": 80,
        "height": 80,
        "original_width": 80,
        "original_height": 80,
        "exif": "{}",
        "sha256": "a567462f4edd496bdf5cd00da5bbde64131c283e3cf396bfd58c0fac26b13d9a",
    },
    {
        "uid": "1e9a6ad5ad6b0a3eef0582b2271c1e8f",
        "face_bboxes": [],
        "caption": "Couleur",
        "url": "https://www.dhresource.com/600x600/f2/albu/g8/M00/78/73/rBVaV150TlWAcLR4AAHizzfChbU318.jpg",
        "key": "000000000004",
        "status": "success",
        "error_message": "",
        "width": 512,
        "height": 384,
        "original_width": 600,
        "original_height": 450,
        "exif": '{"Image Software": "www.meitu.com", "Image ExifOffset": "52", "EXIF ColorSpace": "sRGB", "EXIF ExifImageWidth": "1080", "EXIF ExifImageLength": "1440"}',
        "sha256": "8f1095d595820272bbb79796c67d0cb86e2f8cafa18fd17579d89e3681fa3086",
    },
]


# data that represents metadata and goes to webdataset parquet file of webdataset
# TODO change float values to something other than 0.5 to test if double precision
# works as expected when https://github.com/iterative/datachain/issues/12 is done
WDS_META = {
    "uid": {
        "0": "d142ae70686e14ccc379c01a571501b5",
        "1": "99e71895357f06965a6c5b00d506e5aa",
        "2": "abff9068a3bf22d8325b61a9b1404009",
        "3": "7fa8b7f6ececc9dc80434f3cb6897c27",
        "4": "1e9a6ad5ad6b0a3eef0582b2271c1e8f",
    },
    "url": {
        "0": "https://i.imgur.com/mXQrfNs.png",
        "1": "http://i.ytimg.com/vi/if2V1iszwuA/default.jpg",
        "2": "http://t0.gstatic.com/images?q=tbn:ANd9GcScIHR33LnMpupkxbZRqnj1YMvOXsc9uUTj8Wa2v8bhSjWTxTRo1w",
        "3": "http://thumbs.ebaystatic.com/images/g/5kAAAOSwc1FXcDFI/s-l225.jpg",
        "4": "https://www.dhresource.com/600x600/f2/albu/g8/M00/78/73/rBVaV150TlWAcLR4AAHizzfChbU318.jpg",
    },
    "text": {
        "0": "Customizing Windows 7 Setup Please Help Solved",
        "1": "Jack Strong Official Trailer 1 (2015)   Patrick Wilson Drama Thriller HD",
        "2": "mercedes jeep 2015 mercedes jeep 2015 mercedes g63 amg best images collections",
        "3": "WEN Fall Ginger Pumpkin Cleansing Conditioner ~ 16 oz ~  sealed  plus 6 oz Mist",
        "4": "Couleur",
    },
    "original_width": {
        "0": 1704,
        "1": 120,
        "2": 275,
        "3": 80,
        "4": 600,
    },
    "original_height": {
        "0": 899,
        "1": 90,
        "2": 183,
        "3": 80,
        "4": 450,
    },
    "clip_b32_similarity_score": {
        "0": 0.5,
        "1": 0.5,
        "2": 0.5,
        "3": 0.5,
        "4": 0.5,
    },
    "clip_l14_similarity_score": {
        "0": 0.5,
        "1": 0.5,
        "2": 0.5,
        "3": 0.5,
        "4": 0.5,
    },
    "face_bboxes": {
        "0": [],
        "1": [[0.5, 0.5, 0.5, 0.5]],
        "2": [],
        "3": [],
        "4": [],
    },
    "sha256": {
        "0": "4052f3d8b1f5acee73e234ac8e7c614c5a6e10312d21a65d77b3ffad4edd6b31",
        "1": "9619f8da8b04628994741ed7626d88ace59962824aff43407fee95da488d0ca7",
        "2": "042442926251b1d05345715ea91fb3b2f77b37b2c43af37cbf32cab54a0e6b1a",
        "3": "a567462f4edd496bdf5cd00da5bbde64131c283e3cf396bfd58c0fac26b13d9a",
        "4": "8f1095d595820272bbb79796c67d0cb86e2f8cafa18fd17579d89e3681fa3086",
    },
}
