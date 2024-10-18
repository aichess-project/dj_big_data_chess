import zstandard as zstd
import os
import logging
import time
import logging

logger = logging.getLogger('django')

def remove_zst_extension(filename):
    # Check if the filename ends with '.zst'
    if filename.endswith('.zst'):
        return filename[:-4]  # Remove the last 4 characters
    return filename

def decompress_zst_file(input_folder, output_folder, filename):

    try:
        start_time = time.time()  # Start time for logging execution
        input_file_path = os.path.join(input_folder, filename)
        output_file_path = os.path.join(output_folder, remove_zst_extension(filename))
        with open(input_file_path, 'rb') as compressed_file, open(output_file_path, 'wb') as decompressed_file:
            dctx = zstd.ZstdDecompressor()
            dctx.copy_stream(compressed_file, decompressed_file)
        #os.remove(input_file_path)
        end_time = time.time()  # End time for logging execution
        execution_time = int(end_time - start_time)
        # Check the size of the output file
        output_file_size = int(os.path.getsize(output_file_path))
        logger.info(f'File decompressed successfully: {output_file_path}', extra={'status':'ok', 'operation':'zst_decom_time', 'value': execution_time})
        logger.info(f'File decompressed successfully: {output_file_path}', extra={'status':'ok', 'operation':'zst_decom_file_size', 'value': output_file_size})
        return
    
    except FileNotFoundError as e:
        logger.error(f'File not found: {e}')
    
    except zstd.ZstdError as e:
        logger.error(f'Error decompressing file: {e}')
    
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
    raise Exception("ERROR Decompress ZST File")
