A [Sundai Club](https://sundai.club) project. Vibe coded by Andi Liu, Cyrine, and Debo.

<img width="1125" alt="image" src="https://github.com/user-attachments/assets/117e7b88-461a-42d7-bcc9-c3c2ac7f56b4" />

https://github.com/user-attachments/assets/4bbcf25b-540a-4917-b6c3-45feb15f3eee


# Blog Post to Talking Head Video (Sundai Club)

This repo transforms blog post content into engaging short videos featuring an AI talking head. Users can paste their blog text, potentially add custom notes, review and edit an AI-generated script, and then generate, preview, and download the video (example video in `/public/example_video.mp4`).

## Tech Stack

-   **Framework:** Next.js
-   **UI Components:** shadcn/ui
-   **Video Generation:** HeyGen API
-   **Text Generation:** OpenAI API

## Getting Started

Follow these steps to set up and run the project locally.

### Installation

1.  **Install dependencies:**

    ```bash
    npm install
    ```

2.  **Set up environment variables:**
    Create a file named `.env.local` in the project root and add the following variables:

    ```plaintext
    # .env.local
    OPENAI_API_KEY=your_openai_api_key
    HEYGEN_API_KEY=your_heygen_api_key

    # API URL (Likely for Next.js API routes used internally)
    # Keep default for local development unless your API routes run elsewhere
    NEXT_PUBLIC_API_URL=http://localhost:3000 # Default Next.js port
    ```

    _Replace `your_openai_api_key` and `your_heygen_api_key` with your actual keys._

### Running the Application

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) (or the port specified in the output) in your browser to view the application.
