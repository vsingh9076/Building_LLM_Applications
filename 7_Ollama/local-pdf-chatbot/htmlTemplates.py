"""
This script defines styles and message templates for a chat-like interface.

It includes:

- CSS styles: Define the visual appearance of chat messages for both user and bot.
- bot_template: A formatted HTML string representing a message from the bot.
- user_template: A formatted HTML string representing a message from the user.

You can use these templates within your Streamlit or other web framework application
to create a visually appealing and informative chat interface.
"""

css = """
<style>
  /* Docstring for CSS styles */
  .chat-message {
    /* Styling for chat message containers */
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex; /* Allow avatars and messages side-by-side */
  }

  .chat-message.user {
    /* Styling for user messages */
    background-color: #2b313e; /* Darker blue background */
    color: #fff; /* White text for user messages */
  }

  .chat-message.bot {
    /* Styling for bot messages */
    background-color: #475063; /* Lighter blue background */
    color: #fff; /* White text for bot messages */
  }

  .chat-message .avatar {
    /* Styling for avatar images */
    width: 20%; /* Allocate 20% width for avatars */
  }

  .chat-message .avatar img {
    /* Styling for avatar images within message containers */
    max-width: 78px;
    max-height: 78px;
    border-radius: 50%;
    object-fit: cover;
  }

  .chat-message .message {
    /* Styling for message text */
    width: 80%; /* Allocate 80% width for message content */
    padding: 0 1.5rem; /* Add padding for better readability */
  }
</style>
"""

bot_template = """
<div class="chat-message bot">
  <div class="avatar">
    <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
  </div>
  <div class="message">{{MSG}}</div>
</div>
"""

user_template = """
<div class="chat-message user">
  <div class="avatar">
    <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png">
  </div>
  <div class="message">{{MSG}}</div>
</div>
"""

# UI Improvements (consider implementing these in your application):
# - Allow users to customize avatar images (through file upload or selection)
# - Implement a message input field for user interaction
# - Integrate the templates with your chosen framework to display chat messages
