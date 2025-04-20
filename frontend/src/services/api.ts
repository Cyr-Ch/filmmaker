import axios from 'axios';

// Create axios instance with base URL
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Define API types
export interface ScriptResponse {
  success: boolean;
  script_path: string;
  movie_dir: string;
  title: string;
  error?: string;
}

export interface VideoResponse {
  success: boolean;
  video_path: string;
  error?: string;
}

export interface StylesResponse {
  success: boolean;
  styles: string[];
  error?: string;
}

// API service functions
export const FilmmakerAPI = {
  // Generate script from input text
  generateScript: async (inputText: string): Promise<ScriptResponse> => {
    try {
      const response = await api.post<ScriptResponse>('/generate-script', {
        input_text: inputText,
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        return error.response.data as ScriptResponse;
      }
      return {
        success: false,
        script_path: '',
        movie_dir: '',
        title: '',
        error: 'Network error occurred',
      };
    }
  },

  // Generate video from script text
  generateVideoFromText: async (scriptText: string, videoStyle?: string): Promise<VideoResponse> => {
    try {
      const response = await api.post<VideoResponse>('/generate-video', {
        script_text: scriptText,
        video_style: videoStyle,
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        return error.response.data as VideoResponse;
      }
      return {
        success: false,
        video_path: '',
        error: 'Network error occurred',
      };
    }
  },

  // Generate video from script path
  generateVideoFromPath: async (scriptPath: string, videoStyle?: string): Promise<VideoResponse> => {
    try {
      const response = await api.post<VideoResponse>('/generate-video', {
        script_path: scriptPath,
        video_style: videoStyle,
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        return error.response.data as VideoResponse;
      }
      return {
        success: false,
        video_path: '',
        error: 'Network error occurred',
      };
    }
  },

  // Get available video styles
  getAvailableStyles: async (): Promise<StylesResponse> => {
    try {
      const response = await api.get<StylesResponse>('/available-styles');
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        return error.response.data as StylesResponse;
      }
      return {
        success: false,
        styles: [],
        error: 'Network error occurred',
      };
    }
  },

  // Get file URL from path
  getFileUrl: (filePath: string): string => {
    // Convert the internal file path to a URL path
    // The backend serves files from the /files route
    if (!filePath) return '';
    
    // If the path already starts with http, return it
    if (filePath.startsWith('http')) return filePath;
    
    // Extract the path part after '/files/'
    const filePathMatch = filePath.match(/files\/(.+)$/);
    if (filePathMatch && filePathMatch[1]) {
      return `http://localhost:8000/files/${filePathMatch[1]}`;
    }
    
    // Fallback: just append the full path
    return `http://localhost:8000${filePath}`;
  }
}; 