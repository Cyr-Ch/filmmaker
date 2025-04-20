import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from textwrap import dedent
from datetime import datetime
from typing import Any
from pydantic import BaseModel
from video_helpers.pipeline import pipeline

# Load environment variables
load_dotenv()

class ResultSaver(Agent):
    def __init__(self):
        # Initialize parent class first
        super().__init__(
            role='Result Saver',
            goal='Save outputs from other agents to files',
            backstory="""You are responsible for saving the outputs of other agents to files
            in a structured and organized way. You ensure that all important results are properly
            stored and easily accessible.""",
            verbose=True,
            allow_delegation=False
        )
        # Initialize private attribute after parent class
        self._movie_directory = None

    def set_movie_dir(self, movie_dir):
        self._movie_directory = movie_dir

    def save_result(self, movie_timestamp: str, agent_role: str, content: Any) -> str:
        """Save an agent's output to a file.
        
        Args:
            movie_timestamp: Timestamp identifier for the movie
            agent_role: Role of the agent whose output is being saved
            content: Content to save (can be string or TaskOutput)
            
        Returns:
            Path to the saved file
        """
        if not self._movie_directory:
            raise ValueError("Movie directory not set. Call set_movie_dir first.")

        # Create filename from agent role
        role_to_filename = {
            'Character Designer': 'characters',
            'Music Designer': 'music',
            'Narrator': 'narration',
            'Scene Designer': 'scenes',
            'Story Writer': 'story',
            'Title Generator': 'title'
        }
        filename = f"{role_to_filename.get(agent_role, agent_role.lower().replace(' ', '_'))}.txt"
        
        # Create full path
        filepath = os.path.join(self._movie_directory, filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Write content to file
        with open(filepath, 'w') as f:
            content_str = str(content)
            # Remove triple backticks if present at start and end
            content_str = content_str.strip()
            if content_str.startswith('```') and content_str.endswith('```'):
                content_str = content_str[3:-3].strip()
            f.write(content_str)
            
        return filepath

class MovieScriptGenerator:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.openai_model_name = os.getenv('OPENAI_MODEL_NAME')
        self.movie_dir = None
        self.enable_video = True  # Flag to enable/disable video generation
        self.video_style = os.getenv('VIDEO_STYLE', 'Infinite Zoom')  # Default video style
        
    def create_agents(self):
        # Story Writer Agent
        story_writer = Agent(
            role='Story Writer',
            goal='Write a compelling short movie script with clear scenes and characters',
            backstory="""You are an experienced screenwriter who specializes in creating 
            engaging short films. You focus on creating clear, vivid scenes and memorable characters.""",
            verbose=True,
            allow_delegation=False
        )

        # Title Generator Agent
        title_generator = Agent(
            role='Title Generator',
            goal='Generate a compelling and concise movie title',
            backstory="""You are a creative title specialist who excels at crafting memorable 
            and appropriate titles for movies. You analyze scripts and create titles that capture 
            the essence of the story while being catchy and marketable.""",
            verbose=True,
            allow_delegation=False
        )

        # Character Designer Agent
        character_designer = Agent(
            role='Character Designer',
            goal='Create exactly one image generation prompt per character',
            backstory="""You are an expert at creating precise character descriptions 
            that can be turned into stunning AI-generated images. For each character in 
            the script, you create exactly one detailed prompt that will generate a 
            consistent, high-quality character portrait.""",
            verbose=True,
            allow_delegation=False
        )

        # Scene Designer Agent
        scene_designer = Agent(
            role='Scene Designer',
            goal='Create exactly one image generation prompt per scene with strictly one character per scene, no exceptions',
            backstory="""You are a master of visual storytelling, specializing in creating 
            detailed scene descriptions that can be turned into stunning AI-generated images. 
            For each scene in the script, you create exactly one detailed prompt that will 
            feature strictly one character - no more, no less. Each scene must focus on a single 
            character to maintain simplicity and clarity in the visual narrative.""",
            verbose=True,
            allow_delegation=False
        )

        # Music Designer Agent
        music_designer = Agent(
            role='Music Designer',
            goal='Create music generation prompts for the movie',
            backstory="""You are a skilled music composer who excels at creating prompts 
            for AI music generation. You understand how to match music to the mood and 
            theme of each scene while maintaining consistency throughout the movie.""",
            verbose=True,
            allow_delegation=False
        )

        # Narrator Agent
        narrator = Agent(
            role='Narrator',
            goal='Create SRT subtitles for the movie with precise 5-second scene timing',
            backstory="""You are an expert narrator who creates precisely timed subtitles 
            for movies. You understand how to break down scenes into properly timed 
            segments with clear, engaging narration. You are especially skilled at 
            creating concise narration that fits within strict time constraints, ensuring 
            each scene is exactly 5 seconds or less.""",
            verbose=True,
            allow_delegation=False
        )

        # Result Saver Agent
        result_saver = ResultSaver()

        return story_writer, character_designer, scene_designer, music_designer, narrator, title_generator, result_saver

    def create_tasks(self, story_writer, character_designer, scene_designer, music_designer, narrator, title_generator):
        # Generate movie name and timestamp once for all tasks
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        movie_name = f"movie_{timestamp}"

        # Task 1: Write the script
        write_script = Task(
            description=dedent("""
                Write a short movie script (5 scenes, each scene max 5 seconds).
                Requirements:
                1. Maximum 2 unique characters total for all scenes
                2. Exactly one character per scene - no exceptions
                3. At least one character must appear in multiple scenes
                4. Clear beginning, middle, and end
                5. Scene descriptions with actions and monologues
                
                Output format:
                1. Title
                2. Character list with descriptions (max 2 characters)
                3. 5 scenes with clear descriptions
                4. Exactly one character and their actions/monologue per scene
                5. At least one character appearing in multiple scenes"""),
            agent=story_writer,
            expected_output="""A well-structured movie script containing:
                - Title
                - Character list with descriptions (max 2 characters)
                - 5 scenes with clear descriptions
                - Exactly one character and their actions/monologue per scene
                - At least one character appearing in multiple scenes"""
        )

        # Task 2: Create character prompts
        create_character_prompts = Task(
            description=dedent("""
                Based on the script, create exactly one image generation prompt per character.
                Each prompt should:
                1. Be detailed and consistent with the script
                2. Include physical appearance, clothing, and expression
                3. Specify artistic style and quality parameters"""),
            agent=character_designer,
            expected_output="""A list of image generation prompts:
                - One detailed prompt per character
                - Physical descriptions
                - Clothing and expressions
                - Artistic style specified"""
        )

        # Task 3: Create scene prompts
        create_scene_prompts = Task(
            description=dedent("""
                Create image generation prompts for each scene in the movie.
                Each prompt should:
                1. Start with "Characters in scene: [list all characters present]"
                2. Focus on the main character in that scene
                3. Be consistent with character descriptions
                4. Include setting, lighting, and camera angle
                5. Specify artistic style and quality parameters"""),
            agent=scene_designer,
            expected_output="""A list of image generation prompts:
                - One detailed prompt per scene
                - Explicit list of characters present in the scene
                - Character focus specified
                - Actions and settings detailed"""
        )

        # Task 4: Create music prompt
        create_music_prompt = Task(
            description=dedent("""
                Create music generation prompts for the movie.
                The prompts should:
                1. Match the overall mood and theme
                2. Specify duration, style, and era
                3. Consider scene transitions"""),
            agent=music_designer,
            expected_output="""A list of music generation prompts that:
                - Match movie mood and theme
                - Specify duration and style
                - Consider transitions"""
        )

        # Task 5: Create narration
        create_narration = Task(
            description=dedent(f"""
                Create SRT subtitles for the entire movie, with each scene exactly 5 seconds or less.
                
                Using movie directory: {self.movie_dir}
                1. Create appropriate subtitles that enhance the viewing experience
                2. Ensure each subtitle entry follows proper SRT format with timestamps and sequential numbering
                3. IMPORTANT: Each scene MUST be exactly 5 seconds or less
                
                Each subtitle entry should:
                - Have sequential numbering
                - Include proper timestamps (HH:MM:SS,mmm --> HH:MM:SS,mmm)
                - Contain clear, concise narration text that fits within the 5-second limit
                - Start each new scene at a multiple of 5 seconds (e.g., 00:00:00,000, 00:00:05,000, etc.)"""),
            agent=narrator,
            expected_output="""A complete SRT file with properly formatted subtitle entries, each scene exactly 5 seconds or less."""
        )

        # Task 6: Generate title
        generate_title = Task(
            description=dedent("""
                Based on the script, generate a compelling and concise movie title.
                The title should be memorable, appropriate, and capture the essence of the story.
                Provide ONLY the title, without any additional explanation or formatting."""),
            agent=title_generator,
            expected_output="A concise and compelling movie title"
        )

        return [write_script, create_character_prompts, create_scene_prompts, create_music_prompt, create_narration, generate_title]

    def save_task_result(self, movie_name, task_name, content):
        """Save task result to a file in the appropriate directory."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        directory = os.path.join("files", timestamp + "_" + movie_name)
        os.makedirs(directory, exist_ok=True)
        
        filename = f"{task_name}.txt"
        filepath = os.path.join(directory, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return filepath

    def run(self):
        # Create agents
        story_writer, character_designer, scene_designer, music_designer, narrator, title_generator, result_saver = self.create_agents()
        
        # Create tasks
        tasks = self.create_tasks(story_writer, character_designer, scene_designer, music_designer, narrator, title_generator)
        
        # Create crew and execute
        crew = Crew(
            agents=[story_writer, character_designer, scene_designer, music_designer, narrator, title_generator, result_saver],
            tasks=tasks,
            verbose=True
        )
        
        result = crew.kickoff()
        
        # Get the generated title from the title task
        title_task = tasks[-1]  # Last task is the title generation task
        movie_title = str(title_task.output).strip() if title_task.output else "Untitled"
        
        # Get current timestamp for the movie directory
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Use both timestamp and title in directory name, sanitize the title for filesystem
        safe_title = "".join(c for c in movie_title if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_title = safe_title.replace(' ', '_')
        movie_name = f"{current_time}_{safe_title}"
        self.movie_dir = os.path.join("files", movie_name)
        os.makedirs(self.movie_dir, exist_ok=True)
        
        # Set the movie directory in the result saver
        result_saver.set_movie_dir(self.movie_dir)
        
        # Save results using ResultSaver agent
        for task in tasks:
            if task.output is not None:  # Only save if there's output
                result_saver.save_result(
                    movie_timestamp=current_time,
                    agent_role=task.agent.role,
                    content=task.output
                )
        
        # Generate video if enabled
        if self.enable_video:
            # Find the narrator's output to use as the script
            narrator_output = None
            for task in tasks:
                if task.agent.role == 'Narrator' and task.output is not None:
                    narrator_output = str(task.output)
                    break
            
            if narrator_output:
                # Define output path for the video
                video_output_path = os.path.join(self.movie_dir, f"{safe_title}.mp4")
                
                # Create data directory if it doesn't exist
                os.makedirs("data", exist_ok=True)
                
                # Call the video generation pipeline
                try:
                    print(f"Generating video with style: {self.video_style}")
                    pipeline(narrator_output, video_output_path, self.video_style)
                    print(f"Video generated successfully: {video_output_path}")
                except Exception as e:
                    print(f"Error generating video: {str(e)}")
        
        return result

if __name__ == "__main__":
    generator = MovieScriptGenerator()
    result = generator.run()
    print(result)
