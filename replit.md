# Chat Application

## Overview
A real-time chat application built with Django Channels that allows users to create and join chat rooms. Messages are ephemeral and disappear when all users leave the room.

## Recent Changes (October 24, 2025)
- **Fixed message duplication**: Messages are now saved only once (in `receive()`) instead of once per connected client
- **Implemented ephemeral messages**: Messages are automatically deleted when the last user disconnects from a room
- **Added connection tracking**: Each WebSocket connection is tracked individually by its unique channel_name
- **Added atomic operations**: Used `select_for_update()` with transactions to prevent race conditions during concurrent connections
- **Fixed silent connection handling**: Connections are now tracked immediately upon WebSocket connect (not on first message)
- **Join notifications**: Added pop-up notifications that appear when users join the chat room
- **Modern UI redesign**: Updated to a sleek blue and black glassmorphism theme with enhanced hover effects

## Project Architecture

### Models (ChatApp/models.py)
- **Room**: Represents a chat room
  - `room_name`: Name of the room
  - `active_users`: JSONField storing active connections as `{channel_name: username}`
  - `add_connection()`: Atomically adds a connection to the room
  - `remove_connection()`: Removes a connection and deletes all messages if the room becomes empty

- **Message**: Represents a chat message
  - `room`: Foreign key to Room
  - `sender`: Username of the sender
  - `message`: Message content

### WebSocket Consumer (ChatApp/consumers.py)
- **ChatConsumer**: Handles WebSocket connections
  - Tracks connections on `connect()` (immediately, not on first message)
  - Removes connections on `disconnect()` 
  - Saves messages once per send in `receive()`
  - Uses atomic operations with `select_for_update()` to prevent race conditions

### Views (ChatApp/views.py)
- **CreateRoom**: Creates or joins a room
- **MessageView**: Displays chat messages for a room
- **logout_view**: Removes all user connections and triggers message cleanup if needed

## Key Features
1. **No duplicate messages**: Each message is saved exactly once to the database
2. **Ephemeral messages**: Messages disappear when everyone logs out from the room
3. **Multi-tab support**: Users can open multiple tabs/connections; messages persist until all connections close
4. **Real-time updates**: WebSocket-based real-time message delivery
5. **Thread-safe**: Atomic operations prevent race conditions during concurrent access
6. **Join notifications**: Pop-up notifications alert existing users when someone joins the chat
7. **Modern glassmorphism UI**: Blue and black theme with translucent effects and smooth animations

## Technical Details
- Framework: Django 5.0 with Django Channels
- WebSocket server: Daphne
- Channel layer: InMemoryChannelLayer (for development)
- Database: SQLite (development)
- Connection tracking: By unique channel_name to handle multiple tabs per user

## Running the Application
The application runs on port 5000 using Daphne:
```
daphne -b 0.0.0.0 -p 5000 ChatProject.asgi:application
```
