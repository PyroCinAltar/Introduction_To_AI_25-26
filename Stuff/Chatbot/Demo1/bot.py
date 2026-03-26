"""
================================================================================
ADVANCED CHATBOT WITH INTENT CLASSIFICATION - Bergen Tech CS Introduction to Artificial Intelligence
================================================================================

Welcome, students! This chatbot demonstrates several important programming
concepts that you'll encounter in real-world software development:

CONCEPTS COVERED:
-----------------
1. Object-Oriented Programming (OOP) - Classes, methods, encapsulation
2. Data Classes - A modern Python feature for creating structured data
3. Regular Expressions (Regex) - Pattern matching in text
4. Type Hints - Making code more readable and self-documenting
5. Natural Language Processing (NLP) basics - Intent classification, sentiment
6. Design Patterns - How to structure code for maintainability

HOW TO USE THIS FILE:
--------------------
1. Read through the comments to understand each section
2. Try running the chatbot: python advanced_chatbot_educational.py
3. Experiment by modifying patterns, responses, or adding new intents
4. Use print statements to debug and see how data flows

Let's dive in!
================================================================================
"""

# =============================================================================
# IMPORTS - External libraries and modules we need
# =============================================================================

import re          # Regular Expressions: for pattern matching in text
                   # Example: re.search(r'\bhello\b', 'hello world') finds 'hello'

import random      # For generating random choices
                   # Example: random.choice(['a', 'b', 'c']) returns one randomly

import json        # For working with JSON data (not heavily used here, but common)
                   # JSON is a data format: {"name": "John", "age": 30}

from datetime import datetime  # For working with dates and times
                               # Example: datetime.now() gives current date/time

from collections import defaultdict  # A dict that provides default values
                                      # (imported but not used - left for extension)

from dataclasses import dataclass, field  # Modern way to create data-holding classes
                                           # Reduces boilerplate code significantly

from typing import Optional, Callable  # Type hints for better code documentation
                                        # Optional[str] means "str or None"
                                        # Callable means "a function"


# =============================================================================
# INTENT DATA CLASS
# =============================================================================
# 
# A "data class" is a special kind of class designed primarily to store data.
# The @dataclass decorator automatically creates __init__, __repr__, etc.
#
# WHAT IS AN INTENT?
# ------------------
# In chatbot terminology, an "intent" is what the user is trying to do.
# Examples of intents:
#   - "greeting" -> user wants to say hello
#   - "ask_time" -> user wants to know the time
#   - "jokes"    -> user wants to hear a joke
#
# Each intent has:
#   - patterns: regex patterns to match user input
#   - responses: possible bot responses
#   - keywords: important words associated with this intent
#   - context features: for multi-turn conversations
#   - action: optional function to execute
# =============================================================================

@dataclass
class Intent:
    """
    Represents a single user intent with all its associated data.
    
    Think of this as a "template" for understanding what users might say
    and how the bot should respond.
    
    ATTRIBUTES EXPLAINED:
    ---------------------
    name: str
        A unique identifier for this intent (e.g., 'greeting', 'farewell')
        Used for debugging and logging
    
    patterns: list[str]
        Regular expression patterns that match this intent
        Example: r'\bhello\b' matches the word "hello"
        The r'' prefix means "raw string" - backslashes aren't escape characters
    
    responses: list[str]
        Possible responses the bot can give
        One is chosen randomly to make the bot feel more natural
        Can include placeholders like {bot_name} that get filled in later
    
    keywords: list[str]
        Important words associated with this intent
        Used as a secondary matching method (simpler than regex)
        Example: ['hello', 'hi', 'hey'] for greeting intent
    
    context_set: Optional[str]
        After responding, set this as the current conversation context
        Example: After asking "how are you?", set context to 'asked_user_feeling'
        This helps the bot understand follow-up responses
    
    context_required: Optional[str]
        This intent only matches if the current context matches this value
        Example: "good" only matches as a feeling response if we just asked
    
    action: Optional[Callable]
        A function to execute when this intent is matched
        Used for dynamic responses like calculations
        Callable means "something you can call like a function"
    """
    name: str
    patterns: list[str]
    responses: list[str]
    keywords: list[str] = field(default_factory=list)  # default_factory=list means
                                                        # "create a new empty list"
                                                        # for each instance
    context_set: Optional[str] = None       # Optional means "can be None"
    context_required: Optional[str] = None
    action: Optional[Callable] = None


# =============================================================================
# CONVERSATION CONTEXT CLASS
# =============================================================================
#
# WHY DO WE NEED CONTEXT?
# -----------------------
# Conversations aren't just single messages - they flow! Consider:
#   Bot: "How are you?"
#   User: "Good"
#
# Without context, "Good" could mean anything. But if we remember that we
# just asked "How are you?", we know "Good" is answering that question.
#
# This class manages:
#   - Conversation history (what was said)
#   - Current context (what we're talking about)
#   - User data (things we've learned about the user)
# =============================================================================

class ConversationContext:
    """
    Manages the state and history of a conversation.
    
    This class acts as the "memory" of our chatbot, storing:
    1. What has been said (history)
    2. What we're currently talking about (context)
    3. What we know about the user (user_data)
    
    REAL-WORLD ANALOGY:
    ------------------
    Imagine you're having a conversation with a friend. You remember:
    - What you've talked about (history)
    - The current topic (context)
    - Things you know about them, like their name (user_data)
    
    This class does the same thing for our chatbot!
    """
    
    def __init__(self):
        """
        Initialize a new conversation context.
        
        __init__ is the "constructor" - it runs when you create a new instance:
            context = ConversationContext()  # This calls __init__
        
        We initialize:
        - history: empty list to store conversation exchanges
        - current_context: None (no context yet)
        - user_data: empty dict to store user information
        - session_start: when this conversation began
        """
        self.history = []              # List of {timestamp, user, bot} dicts
        self.current_context = None    # Current conversation topic/state
        self.user_data = {}            # Store things like user's name
        self.session_start = datetime.now()  # When conversation started
    
    def add_exchange(self, user_input: str, bot_response: str):
        """
        Record a conversation exchange (one user message + one bot response).
        
        Parameters:
        -----------
        user_input : str
            What the user said
        bot_response : str
            What the bot replied
        
        Example:
        --------
        context.add_exchange("Hello!", "Hi there!")
        # Now history contains: [{'timestamp': '...', 'user': 'Hello!', 'bot': 'Hi there!'}]
        
        WHY STORE HISTORY?
        ------------------
        - Analytics: See what users commonly ask
        - Debugging: Understand what went wrong in a conversation
        - Context: Reference earlier parts of the conversation
        """
        self.history.append({
            'timestamp': datetime.now().isoformat(),  # ISO format: "2024-01-15T10:30:00"
            'user': user_input,
            'bot': bot_response
        })
    
    def set_context(self, context: str):
        """
        Set the current conversation context.
        
        Parameters:
        -----------
        context : str
            The context identifier (e.g., 'asked_user_feeling')
        
        Example:
        --------
        After bot asks "How are you?", we might call:
            context.set_context('asked_user_feeling')
        
        Now if user says "good", we know it's answering our question!
        """
        self.current_context = context
    
    def clear_context(self):
        """
        Clear the current context (reset to None).
        
        Call this when the current topic of conversation is complete
        and we're ready for something new.
        """
        self.current_context = None
    
    def set_user_data(self, key: str, value):
        """
        Store information about the user.
        
        Parameters:
        -----------
        key : str
            What kind of information (e.g., 'name', 'favorite_color')
        value : any
            The information to store
        
        Example:
        --------
        context.set_user_data('name', 'Alice')
        # Later we can use this to personalize responses!
        """
        self.user_data[key] = value
    
    def get_user_data(self, key: str, default=None):
        """
        Retrieve stored user information.
        
        Parameters:
        -----------
        key : str
            What information to get
        default : any
            Value to return if key doesn't exist (default: None)
        
        Returns:
        --------
        The stored value, or default if not found
        
        Example:
        --------
        name = context.get_user_data('name', 'friend')
        # Returns 'Alice' if we stored it, otherwise 'friend'
        """
        return self.user_data.get(key, default)
    
    def get_last_exchange(self):
        """
        Get the most recent conversation exchange.
        
        Returns:
        --------
        dict or None
            The last exchange, or None if no history exists
        
        Example:
        --------
        last = context.get_last_exchange()
        if last:
            print(f"User last said: {last['user']}")
        """
        return self.history[-1] if self.history else None
        # Note: history[-1] gets the LAST item in the list
        # This is Python's negative indexing feature!


# =============================================================================
# SENTIMENT ANALYZER CLASS
# =============================================================================
#
# WHAT IS SENTIMENT ANALYSIS?
# ---------------------------
# Sentiment analysis determines the emotional tone of text:
#   - Positive: "I love this!", "Great job!", "Thanks so much!"
#   - Negative: "This is terrible", "I hate it", "So frustrating"
#   - Neutral: "The sky is blue", "It's 3 PM", "I went to the store"
#
# WHY IS THIS USEFUL?
# -------------------
# The bot can respond more empathetically:
#   - User seems happy? Match their energy!
#   - User seems upset? Be more gentle and supportive
#
# This is a SIMPLE rule-based approach. Real-world sentiment analysis
# often uses machine learning models trained on millions of examples.
# =============================================================================

class SentimentAnalyzer:
    """
    Simple rule-based sentiment analysis.
    
    This class analyzes text to determine if it's positive, negative, or neutral.
    
    HOW IT WORKS:
    -------------
    1. Split the input text into words
    2. Count how many positive words appear
    3. Count how many negative words appear
    4. Compare the counts to determine overall sentiment
    
    LIMITATIONS:
    ------------
    - Doesn't understand context: "not bad" is positive, but we'd count "bad"
    - Doesn't understand sarcasm: "Oh great, another bug" seems positive
    - Limited vocabulary: only knows words in our lists
    
    For production chatbots, you'd use more sophisticated NLP libraries
    like NLTK, TextBlob, or transformer models.
    """
    
    # CLASS VARIABLES (shared by all instances)
    # These are sets of words associated with each sentiment
    # Using sets (not lists) because checking "is word in set?" is very fast
    
    POSITIVE_WORDS = {
        'good', 'great', 'awesome', 'excellent', 'happy', 'love', 'wonderful',
        'fantastic', 'amazing', 'best', 'nice', 'thank', 'thanks', 'perfect',
        'beautiful', 'brilliant', 'exciting', 'fun', 'glad', 'pleased'
    }
    
    NEGATIVE_WORDS = {
        'bad', 'terrible', 'awful', 'horrible', 'sad', 'hate', 'worst',
        'angry', 'upset', 'annoyed', 'frustrated', 'disappointed', 'boring',
        'stupid', 'dumb', 'useless', 'wrong', 'fail', 'failed', 'problem'
    }
    
    @classmethod  # This decorator means the method belongs to the class, not instances
    def analyze(cls, text: str) -> dict:
        """
        Analyze the sentiment of a text string.
        
        Parameters:
        -----------
        text : str
            The text to analyze
        
        Returns:
        --------
        dict
            {'sentiment': 'positive'/'negative'/'neutral', 'score': float}
            Score ranges from -1 (very negative) to +1 (very positive)
        
        Example:
        --------
        result = SentimentAnalyzer.analyze("I love this amazing chatbot!")
        # Returns: {'sentiment': 'positive', 'score': 0.67}
        
        STEP-BY-STEP EXPLANATION:
        -------------------------
        1. Convert text to lowercase (so "HAPPY" matches "happy")
        2. Split into words
        3. Convert to a set (for fast comparison)
        4. Use set intersection (&) to find matching words
        5. Calculate sentiment based on counts
        """
        # Step 1 & 2: Lowercase and split into words
        words = set(text.lower().split())
        # Example: "I LOVE this!" -> {'i', 'love', 'this!'}
        # Note: This simple split doesn't handle punctuation well
        # A better approach would use proper tokenization
        
        # Step 3: Count positive and negative words using set intersection
        # The & operator finds words that are in BOTH sets
        positive_count = len(words & cls.POSITIVE_WORDS)
        negative_count = len(words & cls.NEGATIVE_WORDS)
        # Example: {'love', 'amazing'} & POSITIVE_WORDS = {'love', 'amazing'}
        
        # Step 4: Determine sentiment based on counts
        if positive_count > negative_count:
            sentiment = 'positive'
            # Score: what fraction of sentiment words are positive?
            # Adding 1 to denominator prevents division by zero
            score = positive_count / (positive_count + negative_count + 1)
        elif negative_count > positive_count:
            sentiment = 'negative'
            # Negative score for negative sentiment
            score = -negative_count / (positive_count + negative_count + 1)
        else:
            sentiment = 'neutral'
            score = 0
        
        return {'sentiment': sentiment, 'score': score}


# =============================================================================
# MAIN CHATBOT CLASS
# =============================================================================
#
# This is where everything comes together! The AdvancedChatbot class:
# 1. Manages intents (what users might want)
# 2. Classifies user input (what do they actually want?)
# 3. Generates appropriate responses
# 4. Maintains conversation context
#
# DESIGN PATTERN: This uses the "Template Method" pattern
# - _setup_intents() defines the structure
# - Each intent is a "template" for handling a type of user input
# =============================================================================

class AdvancedChatbot:
    """
    Advanced chatbot with intent classification and context management.
    
    This is the main class that brings everything together. It:
    1. Holds a collection of intents (possible user goals)
    2. Classifies incoming messages (what does the user want?)
    3. Generates responses based on the matched intent
    4. Manages conversation context for multi-turn dialogue
    
    ARCHITECTURE OVERVIEW:
    ----------------------
    
    User Input
        │
        ▼
    ┌─────────────────┐
    │ classify_intent │ ◄── Finds the best matching intent
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │  get_response   │ ◄── Generates appropriate response
    └────────┬────────┘
             │
             ▼
    Bot Response
    
    HOW TO EXTEND THIS BOT:
    -----------------------
    1. Add new intents in _setup_intents()
    2. Add new response templates
    3. Create custom action functions for complex logic
    """
    
    def __init__(self, name: str = "BERGEN TECH AI"):
        """
        Initialize the chatbot.
        
        Parameters:
        -----------
        name : str
            The chatbot's name (default: "BERGEN TECH AI")
            Used in responses like "I'm {bot_name}!"
        
        What happens during initialization:
        1. Store the bot's name
        2. Create a new conversation context (fresh memory)
        3. Initialize empty intents list
        4. Call _setup_intents() to populate the intents
        """
        self.name = name
        self.context = ConversationContext()  # Create fresh context
        self.intents = []                     # Will hold all Intent objects
        self._setup_intents()                 # Populate the intents list
        # Note: Methods starting with _ are "private" by convention
        # They're meant to be used internally, not called from outside
    
    def _setup_intents(self):
        """
        Initialize all the intents the chatbot can recognize.
        
        This is where we define EVERYTHING our chatbot can understand.
        Each intent represents one type of user goal.
        
        INTENT STRUCTURE REMINDER:
        --------------------------
        Intent(
            name='...',           # Unique identifier
            patterns=[...],       # Regex patterns to match
            keywords=[...],       # Important words
            responses=[...],      # Possible responses
            context_set='...',    # Set this context after responding
            context_required='...', # Only match if in this context
            action=lambda...      # Custom function to execute
        )
        
        REGEX CRASH COURSE:
        -------------------
        \b     = word boundary (start/end of word)
        |      = OR (match this OR that)
        ^      = start of string
        $      = end of string
        (...)  = capture group (extract this part)
        (\w+)  = capture one or more word characters
        ?      = previous char is optional
        .+     = one or more of any character
        \d+    = one or more digits
        """
        
        # -----------------------------------------------------------------
        # GREETING INTENT
        # -----------------------------------------------------------------
        # Matches: "hi", "hello", "hey", "greetings", "howdy", "hola"
        # 
        # Pattern explanation:
        #   r'\b(hi|hello|hey|greetings|howdy|hola)\b'
        #   - \b = word boundary (so "this" doesn't match "hi")
        #   - (a|b|c) = match a OR b OR c
        #   - \b = word boundary again
        # -----------------------------------------------------------------
        self.intents.append(Intent(
            name='greeting',
            patterns=[
                r'\b(hi|hello|hey|greetings|howdy|hola)\b',  # Match greeting words
                r'^(hi|hello|hey)$'  # Match if ONLY "hi", "hello", or "hey"
            ],
            keywords=['hi', 'hello', 'hey', 'greetings'],
            responses=[
                "Hello! Welcome! How can I assist you today?",
                "Hey there! Great to see you. What can I help with?",
                "Hi! I'm {bot_name}, ready to chat. What's on your mind?",
                # Note: {bot_name} is a placeholder that gets replaced later
            ]
        ))
        
        # -----------------------------------------------------------------
        # FAREWELL INTENT
        # -----------------------------------------------------------------
        # Matches: "bye", "goodbye", "see you", "farewell", "quit", "exit"
        # -----------------------------------------------------------------
        self.intents.append(Intent(
            name='farewell',
            patterns=[
                r'\b(bye|goodbye|see you|farewell|quit|exit)\b',
                r'^(bye|quit|exit)$'
            ],
            keywords=['bye', 'goodbye', 'quit', 'exit'],
            responses=[
                "Goodbye! It was great chatting with you!",
                "See you later! Take care!",
                "Farewell! Come back anytime you want to chat!",
            ]
        ))
        
        # -----------------------------------------------------------------
        # BOT NAME INQUIRY INTENT
        # -----------------------------------------------------------------
        # Matches: "what's your name", "who are you", "your name?"
        #
        # Pattern explanation:
        #   r"what('s| is) your name"
        #   - what = literal "what"
        #   - ('s| is) = either "'s" OR " is"
        #   - Matches: "what's your name" or "what is your name"
        # -----------------------------------------------------------------
        self.intents.append(Intent(
            name='ask_bot_name',
            patterns=[
                r"what('s| is) your name",
                r"who are you",
                r"your name\??"  # \?? means the ? is optional
            ],
            keywords=['name', 'who', 'called'],
            responses=[
                "I'm {bot_name}, your AI assistant!",
                "You can call me {bot_name}. Nice to meet you!",
                "My name is {bot_name}. How can I help?",
            ]
        ))
        
        # -----------------------------------------------------------------
        # USER NAME INTENT (with ACTION)
        # -----------------------------------------------------------------
        # Matches: "my name is Alex", "I'm Alex", "call me Alex"
        #
        # This intent has an ACTION - a function that runs when matched.
        # The action extracts the user's name and saves it!
        #
        # Pattern explanation:
        #   r"my name is (\w+)"
        #   - (\w+) = capture group that matches one or more word characters
        #   - This captures the name so we can use it!
        #   - Example: "my name is Alice" -> group(1) = "Alice"
        # -----------------------------------------------------------------
        self.intents.append(Intent(
            name='user_name',
            patterns=[
                r"my name is (\w+)",  # Captures the name
                r"i'm (\w+)",
                r"call me (\w+)",
                r"i am (\w+)"
            ],
            keywords=['name', 'call', 'am'],
            responses=[
                "Nice to meet you, {user_name}! How can I help you today?",
                "Hello {user_name}! Great to have you here.",
                "Welcome, {user_name}! What would you like to chat about?",
            ],
            # ACTION FUNCTION:
            # This lambda function runs when the intent matches
            # - self: the chatbot instance
            # - match: the regex match object (contains captured groups)
            # - match.group(1) gets the first captured group (the name)
            # - .title() capitalizes the first letter: "alice" -> "Alice"
            action=lambda self, match: self.context.set_user_data('name', match.group(1).title())
        ))
        
        # -----------------------------------------------------------------
        # HOW ARE YOU INTENT (with CONTEXT)
        # -----------------------------------------------------------------
        # Matches: "how are you", "how's it going", "how do you feel"
        #
        # This intent SETS CONTEXT after responding.
        # This way, if user next says "good", we know what they mean!
        # -----------------------------------------------------------------
        self.intents.append(Intent(
            name='how_are_you',
            patterns=[
                r"how are you",
                r"how('s| is) it going",
                r"how do you feel",
                r"you doing\??"
            ],
            keywords=['how', 'feeling', 'doing'],
            responses=[
                "I'm doing great, thanks for asking! How about you?",
                "I'm excellent! Ready to help with whatever you need.",
                "Feeling fantastic! What can I do for you today?",
            ],
            context_set='asked_user_feeling'  # Set this context after responding
        ))
        
        # -----------------------------------------------------------------
        # USER FEELING RESPONSE INTENT (CONTEXT-AWARE)
        # -----------------------------------------------------------------
        # Matches: "I'm good", "great", "doing well"
        # BUT ONLY if the current context is 'asked_user_feeling'
        #
        # This demonstrates context-aware matching:
        # - User says "good" after we asked "how are you?" -> matches
        # - User says "good" randomly -> doesn't match (context wrong)
        # -----------------------------------------------------------------
        self.intents.append(Intent(
            name='user_feeling_good',
            patterns=[
                r"i('m| am) (good|great|fine|okay|excellent|happy)",
                r"(good|great|fine|excellent|happy)$",  # Just "good" or "great"
                r"doing (well|good|great)"
            ],
            keywords=['good', 'great', 'fine', 'happy', 'well'],
            responses=[
                "Wonderful to hear! What would you like to talk about?",
                "That's great! Is there anything I can help you with?",
                "Awesome! I'm glad you're doing well.",
            ],
            context_required='asked_user_feeling'  # Only match in this context!
        ))
        
        # -----------------------------------------------------------------
        # TIME INQUIRY INTENT
        # -----------------------------------------------------------------
        self.intents.append(Intent(
            name='ask_time',
            patterns=[
                r"what time is it",
                r"what('s| is) the time",
                r"current time",
                r"tell me the time"
            ],
            keywords=['time', 'clock'],
            responses=[
                "It's currently {current_time}.",
                "The time is {current_time}.",
                "Right now it's {current_time}.",
            ]
        ))
        
        # -----------------------------------------------------------------
        # DATE INQUIRY INTENT
        # -----------------------------------------------------------------
        self.intents.append(Intent(
            name='ask_date',
            patterns=[
                r"what('s| is) the date",
                r"what day is it",
                r"today('s)? date",  # ('s)? means 's is optional
                r"current date"
            ],
            keywords=['date', 'day', 'today'],
            responses=[
                "Today is {current_date}.",
                "It's {current_date}.",
                "The date is {current_date}.",
            ]
        ))
        
        # -----------------------------------------------------------------
        # HELP INTENT
        # -----------------------------------------------------------------
        self.intents.append(Intent(
            name='help',
            patterns=[
                r"\bhelp\b",
                r"what can you do",
                r"capabilities",
                r"features"
            ],
            keywords=['help', 'assist', 'capabilities'],
            responses=[
                """Here's what I can help with:
                
• **Conversation**: Just chat with me about anything!
• **Time & Date**: Ask me what time or date it is
• **Jokes**: I know a few programming jokes
• **Remember Your Name**: Tell me your name, I'll remember it
• **Calculations**: Ask me to calculate something
• **Fun Facts**: Ask me for a random fact

Just type naturally and I'll do my best to understand!""",
            ]
        ))
        
        # -----------------------------------------------------------------
        # JOKES INTENT
        # -----------------------------------------------------------------
        self.intents.append(Intent(
            name='jokes',
            patterns=[
                r"tell (me )?a joke",  # (me )? means "me " is optional
                r"joke",
                r"make me laugh",
                r"something funny"
            ],
            keywords=['joke', 'funny', 'laugh', 'humor'],
            responses=[
                "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
                "Why did the developer go broke? Because he used up all his cache! 💰",
                "A SQL query walks into a bar, approaches two tables, and asks... 'Can I join you?'",
                "Why do Java developers wear glasses? Because they can't C#! 👓",
                "There are only 10 types of people: those who understand binary and those who don't.",
                "Why was the JavaScript developer sad? Because he didn't Node how to Express himself!",
                "What's a programmer's favorite hangout place? Foo Bar! 🍺",
            ]
        ))
        
        # -----------------------------------------------------------------
        # THANKS INTENT
        # -----------------------------------------------------------------
        self.intents.append(Intent(
            name='thanks',
            patterns=[
                r"thank(s| you)",  # "thanks" or "thank you"
                r"thx",
                r"appreciate it",
                r"you('re| are) helpful"
            ],
            keywords=['thanks', 'thank', 'appreciate'],
            responses=[
                "You're welcome! Happy to help! 😊",
                "Anytime! That's what I'm here for.",
                "Glad I could assist!",
                "My pleasure! Let me know if you need anything else.",
            ]
        ))
        
        # -----------------------------------------------------------------
        # CALCULATIONS INTENT (with CUSTOM ACTION)
        # -----------------------------------------------------------------
        # Matches: "calculate 5 + 3", "what's 10 * 2", "15 / 3"
        #
        # This intent has an action that actually performs the calculation!
        #
        # Pattern explanation:
        #   r"(\d+[\s]*[\+\-\*\/][\s]*\d+)"
        #   - \d+ = one or more digits
        #   - [\s]* = zero or more whitespace characters
        #   - [\+\-\*\/] = one of: + - * /
        #   - Example: "5 + 3" or "5+3" or "5  +  3"
        # -----------------------------------------------------------------
        self.intents.append(Intent(
            name='calculate',
            patterns=[
                r"calculate (.+)",  # Capture everything after "calculate"
                r"what('s| is) (\d+[\s]*[\+\-\*\/][\s]*\d+)",
                r"(\d+[\s]*[\+\-\*\/][\s]*\d+)"  # Just the math expression
            ],
            keywords=['calculate', 'math', '+', '-', '*', '/'],
            responses=["Let me calculate that..."],  # Not used when action returns
            action=lambda self, match: self._calculate(match)
        ))
        
        # -----------------------------------------------------------------
        # FUN FACTS INTENT
        # -----------------------------------------------------------------
        self.intents.append(Intent(
            name='fun_fact',
            patterns=[
                r"(tell me )?(a )?fun fact",
                r"random fact",
                r"interesting fact",
                r"did you know"
            ],
            keywords=['fact', 'interesting', 'random'],
            responses=[
                "🎯 Fun fact: Honey never spoils! Archaeologists found 3000-year-old honey in Egyptian tombs that was still perfectly edible.",
                "🎯 Fun fact: Octopuses have three hearts and blue blood!",
                "🎯 Fun fact: The first computer programmer was Ada Lovelace, who wrote algorithms for Charles Babbage's Analytical Engine in the 1840s.",
                "🎯 Fun fact: A group of flamingos is called a 'flamboyance'!",
                "🎯 Fun fact: The shortest war in history lasted 38-45 minutes (between Britain and Zanzibar in 1896).",
                "🎯 Fun fact: Python is named after Monty Python, not the snake!",
            ]
        ))
        
        # -----------------------------------------------------------------
        # ABOUT THE BOT INTENT
        # -----------------------------------------------------------------
        self.intents.append(Intent(
            name='about',
            patterns=[
                r"tell me about yourself",
                r"who made you",
                r"what are you",
                r"are you (a )?(robot|ai|bot)"  # (a )? means "a " is optional
            ],
            keywords=['about', 'yourself', 'made', 'created'],
            responses=[
                "I'm {bot_name}, an AI chatbot built with Python! I can have conversations, tell jokes, remember your name, and help with simple tasks. I'm always learning to be more helpful!",
                "I'm a Python-powered chatbot named {bot_name}. I was created to demonstrate natural language processing concepts. Feel free to test my capabilities!",
            ]
        ))
    
    def _calculate(self, match) -> str:
        """
        Perform a mathematical calculation.
        
        This is a custom action function used by the 'calculate' intent.
        
        Parameters:
        -----------
        match : re.Match
            The regex match object containing the captured expression
        
        Returns:
        --------
        str
            A response string with the calculation result
        
        Example:
        --------
        User: "calculate 5 + 3"
        match.group(1) = "5 + 3"
        Returns: "The result of 5 + 3 is **8**"
        
        SECURITY NOTE:
        --------------
        We use eval() here for simplicity, but it's DANGEROUS in real apps!
        eval() executes arbitrary Python code. A malicious user could input:
            "calculate __import__('os').system('rm -rf /')"
        
        In production, use a proper math parser library like `sympy` or
        write your own safe expression evaluator.
        
        Here, we mitigate risk by:
        1. Removing all characters except digits and basic operators
        2. Still, this is for EDUCATIONAL purposes only!
        """
        try:
            # Extract the expression from the match
            # match.lastindex tells us how many groups were captured
            expression = match.group(1) if match.lastindex else match.group(0)
            
            # SAFETY: Remove anything that's not a digit or basic operator
            # re.sub(pattern, replacement, string) replaces matches with replacement
            # [^\d\+\-\*\/\.\(\)\s] means "anything NOT in this set"
            # This removes letters, special chars, etc.
            expression = re.sub(r'[^\d\+\-\*\/\.\(\)\s]', '', expression)
            
            # Evaluate the expression
            # WARNING: eval() is dangerous! See security note above.
            result = eval(expression)
            
            return f"The result of {expression} is **{result}**"
            
        except Exception:
            # If anything goes wrong, give a helpful error message
            return "I couldn't calculate that. Please use a format like '5 + 3' or '10 * 2'."
    
    def _fill_template(self, response: str) -> str:
        """
        Replace placeholder variables in response templates.
        
        This method takes a response like "Hi {bot_name}!" and replaces
        the placeholder with the actual value.
        
        Parameters:
        -----------
        response : str
            A response template possibly containing placeholders
        
        Returns:
        --------
        str
            The response with all placeholders replaced
        
        Supported placeholders:
        - {bot_name} : The chatbot's name
        - {user_name} : The user's name (or "friend" if unknown)
        - {current_time} : Current time (e.g., "02:30 PM")
        - {current_date} : Current date (e.g., "Monday, January 15, 2024")
        
        Example:
        --------
        template = "Hi {user_name}, I'm {bot_name}!"
        result = _fill_template(template)
        # Returns: "Hi Alice, I'm BERGEN TECH AI!"
        """
        # Define all placeholders and their values
        replacements = {
            '{bot_name}': self.name,
            '{user_name}': self.context.get_user_data('name', 'friend'),
            '{current_time}': datetime.now().strftime('%I:%M %p'),
            '{current_date}': datetime.now().strftime('%A, %B %d, %Y'),
        }
        
        # strftime format codes:
        # %I = hour (12-hour clock, 01-12)
        # %M = minute (00-59)
        # %p = AM/PM
        # %A = full weekday name (Monday, Tuesday, ...)
        # %B = full month name (January, February, ...)
        # %d = day of month (01-31)
        # %Y = full year (2024)
        
        # Replace each placeholder with its value
        for key, value in replacements.items():
            response = response.replace(key, value)
        
        return response
    
    def _score_intent(self, intent: Intent, text: str) -> float:
        """
        Calculate how well a user's text matches an intent.
        
        This is the CORE of intent classification! We score each intent
        against the user's input and pick the highest-scoring one.
        
        Parameters:
        -----------
        intent : Intent
            The intent to score against
        text : str
            The user's input text
        
        Returns:
        --------
        float
            A score indicating match quality (higher = better match)
        
        SCORING SYSTEM:
        ---------------
        - Regex pattern match: +2.0 points per matching pattern
        - Keyword match: +0.5 points per matching keyword
        - Context match: +1.0 bonus if required context matches
        - Context mismatch: 0.5x penalty if context is wrong
        
        Example:
        --------
        User input: "hello there"
        Greeting intent patterns: [r'\bhello\b', r'\bhi\b']
        Greeting intent keywords: ['hello', 'hi', 'hey']
        
        Score = 2.0 (pattern match) + 0.5 (keyword 'hello') = 2.5
        """
        score = 0.0
        text_lower = text.lower()
        
        # Check each regex pattern
        for pattern in intent.patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                score += 2.0  # Pattern matches are worth a lot!
        
        # Check keywords (simpler matching)
        words = set(text_lower.split())
        keyword_matches = len(words & set(intent.keywords))
        score += keyword_matches * 0.5  # Each keyword is worth 0.5
        
        # Handle context requirements
        if intent.context_required:
            if self.context.current_context == intent.context_required:
                score += 1.0  # Bonus for matching context!
            else:
                score *= 0.5  # Penalty for wrong context
        
        return score
    
    def classify_intent(self, text: str) -> tuple[Optional[Intent], Optional[re.Match]]:
        """
        Classify user input into an intent.
        
        This method finds the best matching intent for what the user said.
        
        Parameters:
        -----------
        text : str
            The user's input
        
        Returns:
        --------
        tuple[Optional[Intent], Optional[re.Match]]
            - The best matching Intent (or None if no good match)
            - The regex Match object (or None) for extracting groups
        
        ALGORITHM:
        ----------
        1. Score every intent against the input
        2. Keep track of the highest score
        3. If highest score > 0.5, return that intent
        4. Otherwise, return None (no confident match)
        
        The threshold of 0.5 is a tunable parameter. Higher = stricter matching.
        """
        best_intent = None
        best_score = 0
        best_match = None
        
        # Try every intent
        for intent in self.intents:
            score = self._score_intent(intent, text)
            
            # Is this the best so far?
            if score > best_score:
                best_score = score
                best_intent = intent
                
                # Find the actual regex match (needed for capture groups)
                for pattern in intent.patterns:
                    match = re.search(pattern, text.lower(), re.IGNORECASE)
                    if match:
                        best_match = match
                        break  # Found a match, stop looking
        
        # Only return if score is above threshold
        # Threshold of 0.5 means at least one keyword must match
        return (best_intent, best_match) if best_score > 0.5 else (None, None)
    
    def get_response(self, user_input: str) -> str:
        """
        Generate a response to user input.
        
        This is the main method that produces chatbot responses!
        
        Parameters:
        -----------
        user_input : str
            What the user said
        
        Returns:
        --------
        str
            The chatbot's response
        
        PROCESS:
        --------
        1. Classify the intent (what does user want?)
        2. Analyze sentiment (how is user feeling?)
        3. If intent found:
           a. Execute action if present
           b. Pick random response
           c. Fill in template variables
           d. Update context if needed
        4. If no intent found:
           a. Use sentiment-aware default responses
        """
        # Step 1: Classify intent
        intent, match = self.classify_intent(user_input)
        
        # Step 2: Analyze sentiment (used for fallback responses)
        sentiment = SentimentAnalyzer.analyze(user_input)
        
        # Step 3: Handle matched intent
        if intent:
            # Execute custom action if present
            if intent.action:
                action_result = intent.action(self, match)
                if action_result:
                    return self._fill_template(action_result)
            
            # Pick a random response and fill in templates
            response = random.choice(intent.responses)
            response = self._fill_template(response)
            
            # Update conversation context
            if intent.context_set:
                self.context.set_context(intent.context_set)
            else:
                self.context.clear_context()  # Reset context
            
            return response
        
        # Step 4: No intent matched - use sentiment-aware defaults
        if sentiment['sentiment'] == 'positive':
            defaults = [
                "I love your positive energy! What else is on your mind?",
                "That sounds great! Tell me more.",
                "Wonderful! What else would you like to chat about?",
            ]
        elif sentiment['sentiment'] == 'negative':
            defaults = [
                "I'm sorry to hear that. Is there anything I can help with?",
                "That sounds challenging. Want to talk about it?",
                "I understand. I'm here if you need to chat.",
            ]
        else:
            defaults = [
                "Interesting! Could you tell me more about that?",
                "I see. What else is on your mind?",
                "That's intriguing! Type 'help' to see what I can do.",
                "Hmm, I'm not quite sure what you mean. Try asking differently?",
            ]
        
        return random.choice(defaults)
    
    def chat(self):
        """
        Main interactive chat loop.
        
        This method runs the chatbot in an interactive mode where users
        can type messages and receive responses.
        
        FLOW:
        -----
        1. Print welcome message
        2. Loop forever:
           a. Get user input
           b. Generate response
           c. Save to history
           d. Print response
           e. Check if user wants to exit
        3. Handle Ctrl+C gracefully
        """
        # Print welcome banner
        print(f"\n{'='*60}")
        print(f"  🤖 Welcome! I'm {self.name}, your AI assistant.")
        print(f"  Type 'quit' or 'exit' to end our conversation.")
        print(f"  Type 'help' to see what I can do!")
        print(f"{'='*60}\n")
        
        # Main loop
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()  # .strip() removes whitespace
                
                # Skip empty inputs
                if not user_input:
                    continue
                
                # Generate response
                response = self.get_response(user_input)
                
                # Record the exchange in history
                self.context.add_exchange(user_input, response)
                
                # Print the response
                print(f"\n{self.name}: {response}\n")
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    break
                    
            except KeyboardInterrupt:
                # Handle Ctrl+C gracefully
                print(f"\n\n{self.name}: Goodbye! Thanks for chatting! 👋")
                break
            except Exception as e:
                # Handle any unexpected errors
                print(f"\n{self.name}: Oops, something went wrong. Let's continue!\n")
    
    def get_conversation_history(self) -> list:
        """
        Return the complete conversation history.
        
        Returns:
        --------
        list
            List of exchange dictionaries with 'timestamp', 'user', 'bot' keys
        
        Example:
        --------
        history = bot.get_conversation_history()
        for exchange in history:
            print(f"User: {exchange['user']}")
            print(f"Bot: {exchange['bot']}")
        """
        return self.context.history


# =============================================================================
# MAIN FUNCTION - Entry point of the program
# =============================================================================

def main():
    """
    Run the advanced chatbot.
    
    This is the entry point when you run:
        python advanced_chatbot_educational.py
    
    The if __name__ == "__main__": pattern below ensures this only runs
    when the file is executed directly, not when imported as a module.
    """
    # Create a chatbot instance named "BERGEN TECH AI"
    bot = AdvancedChatbot(name="BERGEN TECH AI")
    
    # Start the interactive chat loop
    bot.chat()
    
    # After chat ends, show session stats
    history = bot.get_conversation_history()
    if history:
        print(f"\n📝 Session had {len(history)} exchanges.")


# This is a common Python pattern:
# __name__ is a special variable that equals "__main__" when the script
# is run directly (not imported). This lets us use this file as both:
# 1. A standalone program (run it directly)
# 2. A module to import (use the classes in other code)

if __name__ == "__main__":
    main()


# =============================================================================
# EXERCISES FOR STUDENTS
# =============================================================================
"""
Now that you understand the code, try these exercises!

EASY:
-----
1. Add a new intent for "weather" that responds with a weather-related message
2. Add more jokes to the jokes intent
3. Change the bot's default name from "BERGEN TECH AI" to something else

MEDIUM:
-------
4. Add a "remember" intent that lets users store arbitrary information:
   User: "Remember that my favorite color is blue"
   Bot: "Got it! I'll remember that your favorite color is blue."
   Later...
   User: "What's my favorite color?"
   Bot: "Your favorite color is blue!"

5. Add more context-aware intents:
   Bot: "Would you like to hear a joke?"
   User: "yes" (should work because of context)

6. Improve the sentiment analyzer to handle negation:
   "not bad" should be positive, not negative

HARD:
-----
7. Add a "quiz" intent that asks trivia questions and tracks score:
   User: "quiz me"
   Bot: "What year did Python first release? (1989, 1991, 1995)"
   User: "1991"
   Bot: "Correct! Score: 1/1"

8. Implement typo tolerance using edit distance:
   User: "helo" should still match "hello"

9. Save conversation history to a JSON file and load it on startup

10. Create a web interface using Flask or FastAPI

BONUS: Understanding ML Chatbots
--------------------------------
This chatbot uses rule-based matching. Modern chatbots use machine learning!
Research these topics:
- TF-IDF (Term Frequency-Inverse Document Frequency) - You will have this question in your QUIZ!
- Word embeddings (Word2Vec, GloVe)
- Transformer models (BERT, GPT)
- Rasa or Dialogflow for production chatbots
"""