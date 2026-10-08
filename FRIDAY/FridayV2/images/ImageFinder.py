from bing_image_downloader import downloader

query_string = "cat photo jpeg -infographic -vector -paw -caterpillar"

downloader.download(query_string, limit=150, output_dir='FRIDAY\FridayV2\images\cat', adult_filter_off=False, force_replace=False, timeout=60, verbose=True, filter="photo")