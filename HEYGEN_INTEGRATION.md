# Heygen Avatar Integration

This document explains how to set up and use the Heygen avatar streaming feature in the Filmmaker application.

## Prerequisites

- A Heygen account with API access
- An API token from Heygen
- Node.js and npm installed

## Setup

1. Install the required dependencies:

```bash
npm install @heygen/streaming-avatar
```

2. Set your Heygen API token in the `.env.local` file:

```
NEXT_PUBLIC_HEYGEN_TOKEN=your-heygen-token-here
```

## How It Works

The Filmmaker application now uses Heygen's streaming avatar technology to create engaging presentations based on text scripts.

1. The user inputs a prompt for the video
2. The system generates a script
3. The user can edit the script and select an avatar
4. The avatar streams the presentation in real-time using the Heygen API

## Components

- `StreamingAvatar.tsx`: The main component that handles the avatar streaming
- `config/api.ts`: Configuration for API tokens and endpoints
- `page.tsx`: The main page that integrates the avatar component

## Avatar Options

The application currently supports three default avatars:
- Anna (Female)
- Alex (Male)
- Skyler (Neutral)

You can add more avatars by modifying the `availableAvatars` state in the `page.tsx` file.

## Customization

You can customize the avatar's appearance and behavior by modifying the StreamingAvatar component or the AVATAR_CONFIG in the config/api.ts file.

## Troubleshooting

If you encounter issues with the avatar streaming:

1. Check that your Heygen API token is valid and correctly set in `.env.local`
2. Ensure you have an active internet connection
3. Check the browser console for any error messages
4. Verify that you have the latest version of the @heygen/streaming-avatar package

## Resources

- [Heygen API Documentation](https://docs.heygen.com/)
- [Streaming Avatar SDK Reference](https://docs.heygen.com/streaming-avatar-sdk) 