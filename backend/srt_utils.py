"""
Utility functions for working with SRT (SubRip) subtitle files.
"""

def format_timestamp(seconds):
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def create_srt_entry(index, start_time, end_time, text):
    """Create a single SRT subtitle entry"""
    # Remove any backticks from the text
    text = text.replace('```', '')
    return f"{index}\n{start_time} --> {end_time}\n{text}\n\n"

def validate_srt(srt_content):
    """
    Validate SRT content format
    Returns tuple (is_valid, error_message)
    """
    lines = srt_content.strip().split('\n')
    if not lines:
        return False, "Empty SRT content"
    
    try:
        entry_count = 1
        i = 0
        while i < len(lines):
            # Skip empty lines
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i >= len(lines):
                break
                
            # Check index
            if not lines[i].strip().isdigit() or int(lines[i]) != entry_count:
                return False, f"Invalid entry index at line {i+1}"
            i += 1
            
            # Check timestamp format
            if i >= len(lines):
                return False, "Unexpected end of file after index"
            timestamp_parts = lines[i].split(' --> ')
            if len(timestamp_parts) != 2:
                return False, f"Invalid timestamp format at line {i+1}"
            i += 1
            
            # Check subtitle text
            if i >= len(lines):
                return False, "Unexpected end of file after timestamp"
            while i < len(lines) and lines[i].strip():
                i += 1
            
            entry_count += 1
            
        return True, "Valid SRT format"
    except Exception as e:
        return False, f"Error validating SRT: {str(e)}"

def save_srt_file(directory, srt_content):
    """
    Save SRT content to a file after validation
    Returns tuple (success, message)
    """
    # Validate SRT content first
    is_valid, message = validate_srt(srt_content)
    if not is_valid:
        return False, f"Invalid SRT content: {message}"
    
    try:
        import os
        filepath = os.path.join(directory, "narration.srt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(srt_content)
        return True, f"Successfully saved SRT file to {filepath}"
    except Exception as e:
        return False, f"Error saving SRT file: {str(e)}"
