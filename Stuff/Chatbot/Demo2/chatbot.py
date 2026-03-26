"""
================================================================================
ADVANCED CHATBOT WITH JSON CONFIGURATION - Bergen Tech CS Introduction to AI
================================================================================
"""

import re
import random
import json
import os
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, Callable, Dict, List, Any
from collections import Counter

@dataclass
class Intent:
    """Represents a single user intent with all its associated data."""

    name: str
    patterns: list
    responses: list
    keywords: list = field(default_factory=list)
    context_set: Optional[str] = None
    context_required: Optional[str] = None
    action: Optional[Callable] = None
    action_type: Optional[str] = None


class ConversationContext:
    """Manages the state and history of a conversation."""

    def __init__(self):
        self.history = []
        self.current_context = None
        self.user_data = {}
        self.session_start = datetime.now()

    def add_exchange(self, user_input: str, bot_response: str):
        self.history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "user": user_input,
                "bot": bot_response,
            }
        )

    def set_context(self, context: str):
        self.current_context = context

    def clear_context(self):
        self.current_context = None

    def set_user_data(self, key: str, value):
        self.user_data[key] = value

    def get_user_data(self, key: str, default=None):
        return self.user_data.get(key, default)

    def get_last_exchange(self):
        return self.history[-1] if self.history else None


class SentimentAnalyzer:
    """Simple rule-based sentiment analysis."""

    POSITIVE_WORDS = set()
    NEGATIVE_WORDS = set()

    @classmethod
    def load_from_config(cls, config: Dict):
        """Load sentiment words from JSON configuration."""
        if "sentiment_words" in config:
            sentiment_config = config["sentiment_words"]
            cls.POSITIVE_WORDS = set(sentiment_config.get("positive", []))
            cls.NEGATIVE_WORDS = set(sentiment_config.get("negative", []))
            print(f"✓ Loaded {len(cls.POSITIVE_WORDS)} positive words")
            print(f"✓ Loaded {len(cls.NEGATIVE_WORDS)} negative words")

    @classmethod
    def analyze(cls, text: str) -> dict:
        """Analyze the sentiment of a text string."""
        words = set(text.lower().split())
        positive_count = len(words & cls.POSITIVE_WORDS)
        negative_count = len(words & cls.NEGATIVE_WORDS)

        if positive_count > negative_count:
            sentiment = "positive"
            score = positive_count / (positive_count + negative_count + 1)
        elif negative_count > positive_count:
            sentiment = "negative"
            score = -negative_count / (positive_count + negative_count + 1)
        else:
            sentiment = "neutral"
            score = 0

        return {"sentiment": sentiment, "score": score}


class ConfigLoader:
    """Handles loading and validating JSON configuration files."""
    @staticmethod
    def load_config(filepath: str) -> Dict:
        """Load and parse a JSON configuration file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Configuration file '{filepath}' not found!")

        with open(filepath, "r", encoding="utf-8") as f:
            config = json.load(f)
        print(f"✓ Successfully loaded configuration from '{filepath}'")
        return config

    @staticmethod
    def validate_config(config: Dict) -> bool:
        """Validate that the configuration has all required sections."""
        required_sections = ["bot_settings", "intents"]

        for section in required_sections:
            if section not in config:
                raise ValueError(f"Missing required section '{section}'")

        required_intent_fields = ["name", "patterns", "responses"]
        for i, intent in enumerate(config["intents"]):
            for fld in required_intent_fields:
                if fld not in intent:
                    raise ValueError(f"Intent #{i} missing field '{fld}'")

        print(f"✓ Configuration validated successfully")
        print(f"✓ Found {len(config['intents'])} intents")
        return True


class AdvancedChatbot:
    """Advanced chatbot with JSON-based intent configuration."""

    def __init__(self, config_path: str = "chatbot_intents.json", name: str = None):
        """Initialize the chatbot with JSON configuration."""
        print("\n" + "=" * 50)
        print("🤖 Initializing BERGEN TECH AI Chatbot")
        print("=" * 50)

        self.config = ConfigLoader.load_config(config_path)
        ConfigLoader.validate_config(self.config)

        bot_settings = self.config.get("bot_settings", {})
        self.name = name or bot_settings.get("default_name", "BERGEN TECH AI")
        self.exit_commands = bot_settings.get("exit_commands", ["quit", "exit"])

        self.unknown_responses = {
            "positive": bot_settings.get(
                "unknown_response_positive", ["That's great!"]
            ),
            "negative": bot_settings.get(
                "unknown_response_negative", ["I'm sorry to hear that."]
            ),
            "neutral": bot_settings.get("unknown_response_neutral", ["Interesting!"]),
        }

        SentimentAnalyzer.load_from_config(self.config)

        self.intents = []
        self.context = ConversationContext()
        self._build_intents()

        print("=" * 50)
        print("✓ Chatbot initialization complete!")
        print("=" * 50 + "\n")

    def _build_intents(self):
        """Build Intent objects from JSON configuration."""
        for intent_data in self.config["intents"]:
            action_func = None
            action_type = intent_data.get("action_type")

            # FIXED: Use factory methods instead of lambdas to avoid closure issues
            if action_type == "store_user_name":
                action_func = self._create_store_name_action()
            elif action_type == "calculate":
                action_func = self._create_calculate_action()
            elif action_type == "store_user_birthday":
                action_func = self._create_store_birthday_action()
            elif action_type == "store_user_note":
                action_func = self._create_save_note_action()
            elif action_type == "show_user_notes":
                action_func = self._create_show_notes_action()
            elif action_type == "add_favorites":
                action_func = self._create_store_favorites_action()



            intent = Intent(
                name=intent_data["name"],
                patterns=intent_data["patterns"],
                responses=intent_data["responses"],
                keywords=intent_data.get("keywords", []),
                context_set=intent_data.get("context_set"),
                context_required=intent_data.get("context_required"),
                action=action_func,
                action_type=action_type,
            )
            self.intents.append(intent)
            

        print(f"✓ Built {len(self.intents)} intent handlers")

    def _create_store_name_action(self):
        """Factory method to create the store_user_name action."""

        def store_name_action(chatbot, match):
            if match and match.lastindex and match.lastindex >= 1:
                name = match.group(1).title()
                chatbot.context.set_user_data("name", name)
            return None  # Return None so normal response flow continues

        return store_name_action

    def _create_calculate_action(self):
        """Factory method to create the calculate action."""

        def calculate_action(chatbot, match):
            return chatbot._calculate(match)

        return calculate_action

    def _calculate(self, match) -> str:
        """Perform a mathematical calculation."""
        try:
            expression = match.group(1) if match.lastindex else match.group(0)
            expression = re.sub(r"[^\d\+\-\*\/\.\(\)\s]", "", expression)
            result = eval(expression)
            return f"The result of {expression} is **{result}**"
        except Exception:
            return "I couldn't calculate that. Please use a format like '5 + 3' or '10 * 2'."

    def _fill_template(self, response: str) -> str:
        """Replace placeholder variables in response templates."""
        replacements = {
            "{bot_name}": self.name,
            "{user_name}": self.context.get_user_data("name", "friend"),
            "{current_time}": datetime.now().strftime("%I:%M %p"),
            "{current_date}": datetime.now().strftime("%A, %B %d, %Y"), 
            "{user_birthday}": self.context.get_user_data("birthday", "unknown"),
        }

        for key, value in replacements.items():
            response = response.replace(key, value)

        return response

    def _score_intent(self, intent: Intent, text: str) -> float:
        """Calculate how well a user's text matches an intent."""
        score = 0.0
        text_lower = text.lower()

        for pattern in intent.patterns:
            try:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    score += 2.0
            except re.error:
                continue

        text_words = set(text_lower.split())
        for keyword in intent.keywords:
            if keyword.lower() in text_words:
                score += 0.5

        if intent.context_required:
            if self.context.current_context == intent.context_required:
                score += 1.0
            else:
                score *= 0.5

        return score

    def classify_intent(self, text: str):
        """Find the best matching intent for user input."""
        best_intent = None
        best_score = 0.0
        best_match = None

        for intent in self.intents:
            score = self._score_intent(intent, text)

            if score > best_score:
                best_score = score
                best_intent = intent

                for pattern in intent.patterns:
                    try:
                        match = re.search(pattern, text.lower(), re.IGNORECASE)
                        if match:
                            best_match = match
                            break
                    except re.error:
                        continue

        if best_score > 0.5:
            return best_intent, best_match
        return None, None

    def get_response(self, user_input: str) -> str:
        """Generate a response to user input."""
        intent, match = self.classify_intent(user_input)
        sentiment = SentimentAnalyzer.analyze(user_input)

        if intent:
            # Execute custom action if present
            if intent.action:
                action_result = intent.action(self, match)
                if action_result:
                    return self._fill_template(action_result)

            # Pick a random response and fill templates
            response = random.choice(intent.responses)
            response = self._fill_template(response)

            # Update context
            if intent.context_set:
                self.context.set_context(intent.context_set)
            else:
                self.context.clear_context()

            return response

        # Use sentiment-aware defaults
        sentiment_type = sentiment["sentiment"]
        return random.choice(
            self.unknown_responses.get(
                sentiment_type, self.unknown_responses["neutral"]
            )
        )

    def chat(self):
        """Main interactive chat loop."""
        print(f"\n{'='*60}")
        print(f"  🤖 Welcome! I'm {self.name}, your AI assistant.")
        print(f"  Type 'quit' or 'exit' to end our conversation.")
        print(f"  Type 'help' to see what I can do!")
        print(f"  Type 'stats' to see conversation statistics!")
        print(f"{'='*60}\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() == "stats":
                    self._show_stats()
                    continue

                response = self.get_response(user_input)
                self.context.add_exchange(user_input, response)
                print(f"\n{self.name}: {response}\n")

                if user_input.lower() in self.exit_commands:
                    break

            except KeyboardInterrupt:
                print(f"\n\n{self.name}: Goodbye! Thanks for chatting! 👋")
                break
            except Exception as e:
                print(f"\n{self.name}: Oops, something went wrong. Let's continue!\n")

    def _show_stats(self):
        """Display conversation statistics."""
        history = self.context.history
        print(f"\n{'='*40}")
        print("📊 CONVERSATION STATISTICS")
        print(f"{'='*40}")
        print(f"Total exchanges: {len(history)}")

        if history:
            user_lengths = [len(h["user"]) for h in history]
            bot_lengths = [len(h["bot"]) for h in history]
            print(
                f"Avg user message length: {sum(user_lengths)/len(user_lengths):.0f} chars"
            )
            print(
                f"Avg bot response length: {sum(bot_lengths)/len(bot_lengths):.0f} chars"
            )

        user_data = self.context.user_data
        if user_data:
            print(f"\nKnown about you:")
            for key, value in user_data.items():
                print(f"  • {key}: {value}")
            
            
        sentiment_scores = []
        for exchange in self.context.history:
            analysis = SentimentAnalyzer.analyze(exchange["user"])
        sentiment_scores.append(analysis["score"])

        avg = 0
        if sentiment_scores:
            try:
                avg = round((sum(sentiment_scores)/len(sentiment_scores)), 2)
            except ZeroDivisionError:
                avg = 0
            
            print(f"Average Sentiment Score: {avg}")


        #  Commonly used words(top 3)
        word_counts = {}
        for exchange in self.context.history:
            words = re.findall(r"\b\w+\b", exchange["user"].lower())
            for word in words:
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1
            
        #Getting the top 3
        top_3 = sorted(
            word_counts.items(),
            key=lambda item: item[1],
            reverse=True
            )[:3]
        print("\n🗣️ MOST COMMON WORDS")
        for word, count in top_3:
            print(f"  • {word}: {count} times")
        print()

        # most Intent used (use a count, take first one)
        #Tracking intent usage
        intent_counts = {}

        for exchange in self.context.history:
            # Classify intent for this message
            intent, match = self.classify_intent(exchange["user"])
            if intent:
                name = intent.name
                if name in intent_counts:
                    intent_counts[name] += 1
                else:
                    intent_counts[name] = 1
        #finding most used intent
        most_used_intent = None

        if intent_counts:
            # Sort by count descending, pick first one
            most_used_intent = sorted(
                intent_counts.items(),
                key=lambda item: item[1],  # sort by count
                reverse=True
            )[0][0]  # get the name of the intent
        



        # Conversation duration
        from datetime import datetime

        start = self.context.session_start
        end = datetime.now()

        duration = end - start  # this is a timedelta object
        
        total_seconds = int(duration.total_seconds())
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)

        print(f"⏱️ Conversation duration: {hours}h {minutes}m {seconds}s")

        
    



        print(f"{'='*40}\n")

    def get_conversation_history(self) -> list:
        """Return the complete conversation history."""
        return self.context.history

    def save_conversation(self, filepath: str = "conversation_history.json"):
        """Save conversation history to a JSON file."""
        data = {
            "session_start": self.context.session_start.isoformat(),
            "session_end": datetime.now().isoformat(),
            "bot_name": self.name,
            "user_data": self.context.user_data,
            "history": self.context.history,
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✓ Conversation saved to '{filepath}'")
        
    def _create_store_birthday_action(self):
        """Store the user birthday."""
        def store_birthday_action(chatbot, match):
            if match and match.lastindex >= 1:
                birthday = match.group(1).strip()
                chatbot.context.set_user_data("birthday", birthday)
            return None 
        return store_birthday_action
    
    def _create_save_note_action(self):
        def save_note_action(chatbot, match):
            if match and match.lastindex >= 1:
                note = match.group(1).strip()
                notes = chatbot.context.get_user_data("notes") or []
                notes.append(note)

                chatbot.context.set_user_data("notes", notes)
            return None

        return save_note_action

    
    def _create_show_notes_action(self):
        def show_notes_action(chatbot, match):
            notes = chatbot.context.get_user_data("notes")

            if not notes:
                return "You don't have any saved notes yet."

            formatted_notes = "\n".join(
                [f"{i+1}. {note}" for i, note in enumerate(notes)]
            )
            return f"Here are your saved notes:\n{formatted_notes}"

        return show_notes_action
    
    
    def store_favorites(self, favorite_type: str, favorite_value: str):

        favorites = self.context.get_user_data("favorites", {})

        if favorite_type == "band":
            favorite_type = "music"
        

        favorites[favorite_type] = favorite_value
        

        self.context.set_user_data("favorites", favorites)

        self.context.set_user_data(f"favorite_{favorite_type}", favorite_value)

    def _create_store_favorites_action(self):
        def store_favorites_action(chatbot, match):
            if match and match.lastindex >= 2:

                favorite_type = match.group(1).strip().lower()

                favorite_value = match.group(2).strip()
                

                chatbot.store_favorites(favorite_type, favorite_value)
                
                chatbot.context.set_user_data("favorite_type", favorite_type)
            return None 
        
        return store_favorites_action




def main():
    """Run the advanced chatbot with JSON configuration."""
    try:
        bot = AdvancedChatbot(config_path="chatbot_intents.json")
        bot.chat()

        history = bot.get_conversation_history()
        if history:
            print(f"\n📝 Session had {len(history)} exchanges.")
            save = (
                input("Would you like to save this conversation? (y/n): ")
                .strip()
                .lower()
            )
            if save == "y":
                bot.save_conversation()

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure 'chatbot_intents.json' is in the same directory!")
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON Error: {e}")
        print("\nCheck your JSON file for syntax errors!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
    
