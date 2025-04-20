import os
import json
import tempfile
from typing import Optional, List, Dict, Any, Union
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from filmcrew import MovieScriptGenerator

app = FastAPI(title="Filmmaker API", description="API for generating movie scripts and videos")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directories
# First make sure the files directory exists
os.makedirs("files", exist_ok=True)
app.mount("/files", StaticFiles(directory="files"), name="files")

# Request and Response models
class ScriptRequest(BaseModel):
    input_text: str = Field(..., description="Text prompt for script generation")

class ScriptResponse(BaseModel):
    success: bool = True
    script_path: str
    movie_dir: str
    title: str

class VideoRequestByText(BaseModel):
    script_text: str = Field(..., description="Full SRT format script text")
    video_style: Optional[str] = Field(None, description="Style of video generation")

class VideoRequestByPath(BaseModel):
    script_path: str = Field(..., description="Path to existing script file")
    video_style: Optional[str] = Field(None, description="Style of video generation")

class VideoResponse(BaseModel):
    success: bool = True
    video_path: str

class StylesResponse(BaseModel):
    success: bool = True
    styles: List[str]

class ErrorResponse(BaseModel):
    success: bool = False
    error: str

@app.post("/api/generate-script", response_model=ScriptResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def generate_script(request: ScriptRequest):
    """
    Generate a movie script from input text
    """
    try:
        # Initialize the MovieScriptGenerator
        generator = MovieScriptGenerator()
        
        # Generate the script
        result = generator.run(input_text=request.input_text)
        
        # Return the result
        return {
            "success": True,
            "script_path": result["script_path"],
            "movie_dir": result["movie_dir"],
            "title": result["title"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-video", response_model=VideoResponse, responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def generate_video(
    request_by_text: VideoRequestByText = None,
    request_by_path: VideoRequestByPath = None
):
    """
    Generate a video from a script
    
    You can provide either:
    - script_text: The full SRT format script text
    - script_path: Path to an existing script file
    
    Optionally include video_style to specify the style of video generation
    """
    try:
        # Initialize the MovieScriptGenerator
        generator = MovieScriptGenerator()
        
        # Determine which request model was used
        if request_by_text is not None and request_by_text.script_text:
            # Script text is provided directly
            script_text = request_by_text.script_text
            video_style = request_by_text.video_style
            
            # Create a temporary file to store the script
            temp_dir = tempfile.mkdtemp()
            script_path = os.path.join(temp_dir, 'script.txt')
            
            # Write the script text to the temporary file
            with open(script_path, 'w') as f:
                f.write(script_text)
                
            # Generate the video
            video_path = generator.generate_video_from_script(script_path, video_style)
            
        elif request_by_path is not None and request_by_path.script_path:
            # Path to existing script is provided
            script_path = request_by_path.script_path
            video_style = request_by_path.video_style
            
            # Validate that the path exists
            if not os.path.exists(script_path):
                raise HTTPException(
                    status_code=404, 
                    detail=f"Script file not found at: {script_path}"
                )
                
            # Generate the video
            video_path = generator.generate_video_from_script(script_path, video_style)
            
        else:
            raise HTTPException(
                status_code=400, 
                detail="Either script_text or script_path is required"
            )
        
        # Return the result
        return {
            "success": True,
            "video_path": video_path
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/available-styles", response_model=StylesResponse)
async def get_available_styles():
    """
    Get list of available video styles
    """
    # This is a placeholder - you may need to modify this to get actual styles
    # from your video generation system
    styles = [
        "Infinite Zoom",
        "Pan Left",
        "Pan Right",
        "Pan Up",
        "Pan Down",
        "Zoom In",
        "Zoom Out",
        "Static"
    ]
    
    return {
        "success": True,
        "styles": styles
    }

# For direct execution
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 