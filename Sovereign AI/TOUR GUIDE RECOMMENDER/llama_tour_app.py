import streamlit as st
import requests
import json
from typing import List, Dict, Any
import time

# Page configuration
st.set_page_config(
    page_title="AI-Powered India Tour Guide",
    page_icon="🤖🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
    }
    .recommendation-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .ai-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border-left: 4px solid #FF6B35;
    }
    .user-input-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def call_llama_api(user_profile: Dict[str, Any]) -> str:
    """
    Call Llama 3.2 API to get personalized recommendations
    """
    # Create the prompt for Llama 3.2
    prompt = f"""
    You are an expert travel guide for India. Based on the following user profile, provide personalized travel recommendations:

    USER PROFILE:
    - Name: {user_profile.get('name', 'Traveler')}
    - Age: {user_profile.get('age', 'Not specified')}
    - Budget: {user_profile.get('budget', 'Not specified')}
    - Travel Duration: {user_profile.get('duration', 'Not specified')}
    - Interests: {', '.join(user_profile.get('interests', []))}
    - Preferred States: {', '.join(user_profile.get('states', []))}
    - Travel Style: {user_profile.get('travel_style', 'Not specified')}
    - Group Size: {user_profile.get('group_size', 'Not specified')}
    - Season: {user_profile.get('season', 'Not specified')}

    Please provide:
    1. Top 5 personalized destination recommendations
    2. For each destination: name, state, why it's perfect for this user, best time to visit, estimated budget
    3. Travel tips specific to this user's profile
    4. Hidden gems that match their interests

    Format your response as JSON with this structure:
    {{
        "recommendations": [
            {{
                "name": "Destination Name",
                "state": "State Name",
                "description": "Why it's perfect for this user",
                "best_time": "Best time to visit",
                "estimated_budget": "Budget estimate",
                "highlights": ["highlight1", "highlight2"],
                "relevance_score": 9
            }}
        ],
        "travel_tips": ["tip1", "tip2"],
        "hidden_gems": ["gem1", "gem2"]
    }}

    Be specific, personalized, and practical. Consider the user's age, budget, and interests.
    """

    try:
        # For demo purposes, we'll simulate Llama API response
        # In production, replace this with actual API call to Llama 3.2
        # Example: response = requests.post("LLAMA_API_ENDPOINT", json={"prompt": prompt})
        
        # Simulated response for demo
        time.sleep(2)  # Simulate API call delay
        
        # Generate mock response based on user interests
        interests = user_profile.get('interests', [])
        states = user_profile.get('states', [])
        
        mock_response = generate_mock_response(interests, states, user_profile)
        
        return mock_response
        
    except Exception as e:
        st.error(f"Error calling AI: {str(e)}")
        return get_fallback_response()

def generate_mock_response(interests: List[str], states: List[str], user_profile: Dict) -> str:
    """Generate mock AI response for demo purposes"""
    
    # Destination templates based on interests
    destination_templates = {
        'temples': [
            {
                'name': 'Kedarnath Temple',
                'state': 'Uttarakhand' if not states or 'Uttarakhand' in states else states[0],
                'description': 'Ancient Shiva temple perfect for spiritual seekers',
                'best_time': 'May to October',
                'estimated_budget': '₹5,000-10,000',
                'highlights': ['Spiritual experience', 'Mountain views', 'Char Dham yatra'],
                'relevance_score': 10
            },
            {
                'name': 'Meenakshi Temple',
                'state': 'Tamil Nadu' if not states or 'Tamil Nadu' in states else (states[1] if len(states) > 1 else states[0]),
                'description': 'Architectural marvel with thousands of sculptures',
                'best_time': 'October to March',
                'estimated_budget': '₹3,000-7,000',
                'highlights': ['Dravidian architecture', 'Cultural experience', 'Artisans'],
                'relevance_score': 9
            }
        ],
        'beaches': [
            {
                'name': 'Baga Beach',
                'state': 'Goa' if not states or 'Goa' in states else states[0],
                'description': 'Vibrant beach with water sports and nightlife',
                'best_time': 'November to February',
                'estimated_budget': '₹8,000-15,000',
                'highlights': ['Water sports', 'Nightlife', 'Beach shacks'],
                'relevance_score': 9
            },
            {
                'name': 'Varkala Beach',
                'state': 'Kerala' if not states or 'Kerala' in states else (states[1] if len(states) > 1 else states[0]),
                'description': 'Cliff beach with natural springs and spiritual vibe',
                'best_time': 'September to March',
                'estimated_budget': '₹6,000-12,000',
                'highlights': ['Cliff views', 'Natural springs', 'Yoga centers'],
                'relevance_score': 8
            }
        ],
        'adventure': [
            {
                'name': 'Rishikesh',
                'state': 'Uttarakhand' if not states or 'Uttarakhand' in states else states[0],
                'description': 'Adventure capital with rafting and camping',
                'best_time': 'March to June, September to November',
                'estimated_budget': '₹7,000-14,000',
                'highlights': ['White water rafting', 'Camping', 'Yoga retreats'],
                'relevance_score': 10
            },
            {
                'name': 'Manali',
                'state': 'Himachal Pradesh' if not states or 'Himachal Pradesh' in states else (states[1] if len(states) > 1 else states[0]),
                'description': 'Hill station with snow activities and trekking',
                'best_time': 'December to February for snow, March to June for adventure',
                'estimated_budget': '₹10,000-20,000',
                'highlights': ['Snow activities', 'Trekking', 'Cafe culture'],
                'relevance_score': 9
            }
        ],
        'historical': [
            {
                'name': 'Taj Mahal',
                'state': 'Uttar Pradesh' if not states or 'Uttar Pradesh' in states else states[0],
                'description': 'Iconic monument of love and architectural wonder',
                'best_time': 'October to March',
                'estimated_budget': '₹3,000-8,000',
                'highlights': ['Architectural marvel', 'Photography', 'History'],
                'relevance_score': 10
            },
            {
                'name': 'Hawa Mahal',
                'state': 'Rajasthan' if not states or 'Rajasthan' in states else (states[1] if len(states) > 1 else states[0]),
                'description': 'Palace of Winds with unique honeycomb architecture',
                'best_time': 'November to February',
                'estimated_budget': '₹2,000-5,000',
                'highlights': ['Architecture', 'City views', 'Shopping'],
                'relevance_score': 8
            }
        ]
    }
    
    # Build recommendations based on user interests
    recommendations = []
    interest_lower = [interest.lower() for interest in interests]
    
    for interest in interest_lower:
        for key, destinations in destination_templates.items():
            if key in interest or interest in key:
                recommendations.extend(destinations)
                break
    
    # If no specific interests, add general recommendations
    if not recommendations:
        recommendations = [
            {
                'name': 'Golden Triangle',
                'state': 'Delhi-Agra-Jaipur',
                'description': 'Perfect introduction to India\'s culture and history',
                'best_time': 'October to March',
                'estimated_budget': '₹15,000-25,000',
                'highlights': ['Multiple cities', 'Historical monuments', 'Cultural experience'],
                'relevance_score': 8
            }
        ]
    
    # Limit to top 5 recommendations
    recommendations = recommendations[:5]
    
    # Generate travel tips based on user profile
    travel_tips = [
        f"Book accommodations in advance for {user_profile.get('season', 'peak season')}",
        f"Carry {get_clothing_advice(user_profile.get('season', 'winter'))}",
        "Keep digital copies of important documents",
        "Try local cuisine for authentic experience",
        "Respect local customs and traditions"
    ]
    
    # Generate hidden gems
    hidden_gems = [
        "Spiti Valley for offbeat Himalayan experience",
        "Majuli Island in Assam - world\'s largest river island",
        "Gandikota in Andhra Pradesh - Grand Canyon of India",
        "Chembra Peak in Kerala - heart-shaped lake",
        "Dhanushkodi in Tamil Nadu - ghost town at India\'s tip"
    ]
    
    response = {
        "recommendations": recommendations,
        "travel_tips": travel_tips[:3],
        "hidden_gems": hidden_gems[:2]
    }
    
    return json.dumps(response, indent=2)

def get_clothing_advice(season: str) -> str:
    """Get clothing advice based on season"""
    season_advice = {
        'summer': 'light cotton clothes and sunscreen',
        'winter': 'warm layers and woolens',
        'monsoon': 'raincoat and quick-dry clothes',
        'spring': 'light layers for changing weather'
    }
    return season_advice.get(season.lower(), 'comfortable traveling clothes')

def get_fallback_response() -> str:
    """Fallback response when AI fails"""
    fallback = {
        "recommendations": [
            {
                "name": "Taj Mahal",
                "state": "Uttar Pradesh",
                "description": "Iconic monument of love, must-visit for everyone",
                "best_time": "October to March",
                "estimated_budget": "₹3,000-8,000",
                "highlights": ["Architecture", "History", "Photography"],
                "relevance_score": 10
            }
        ],
        "travel_tips": ["Plan in advance", "Stay hydrated", "Respect local culture"],
        "hidden_gems": ["Explore local markets", "Try street food"]
    }
    return json.dumps(fallback, indent=2)

def main():
    # Title and introduction
    st.markdown('<h1 class="main-header">🤖 AI-Powered India Tour Guide</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #666; margin-bottom: 2rem;">
        Get personalized travel recommendations powered by Llama 3.2 AI
    </div>
    """, unsafe_allow_html=True)
    
    # User Profile Collection
    st.markdown("## 🧭 Tell Us About Your Travel Plans")
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Your Name", placeholder="Enter your name")
            age = st.selectbox("Age Group", ["18-25", "26-35", "36-45", "46-55", "55+"])
            budget = st.selectbox("Budget Range", ["₹5,000-10,000", "₹10,000-25,000", "₹25,000-50,000", "₹50,000+"])
            duration = st.selectbox("Trip Duration", ["Weekend (2-3 days)", "Week (4-7 days)", "2 Weeks (8-14 days)", "Month (15+ days)"])
        
        with col2:
            travel_style = st.selectbox("Travel Style", ["Budget Backpacker", "Mid-range Comfort", "Luxury Traveler", "Family Vacation"])
            group_size = st.selectbox("Group Size", ["Solo", "Couple", "Family with Kids", "Group of Friends"])
            season = st.selectbox("Travel Season", ["Summer (Mar-Jun)", "Monsoon (Jul-Sep)", "Winter (Oct-Feb)", "Spring (Feb-Mar)"])
        
        # Interests (multi-select)
        st.markdown("### 🎯 What are your interests?")
        interest_options = [
            "Temples & Spirituality", "Beaches & Coastal", "Mountains & Hills", "Adventure Sports",
            "Historical Monuments", "Wildlife & Nature", "Food & Cuisine", "Shopping & Markets",
            "Nightlife & Parties", "Yoga & Wellness", "Photography", "Cultural Experiences",
            "Backwaters & Lakes", "Desert Experience", "Trekking & Hiking", "Local Festivals"
        ]
        
        interests = st.multiselect(
            "Select your interests (choose multiple)",
            interest_options,
            default=["Historical Monuments", "Cultural Experiences"]
        )
        
        # Preferred States
        st.markdown("### 🗺️ Which states interest you?")
        state_options = [
            "Uttarakhand", "Himachal Pradesh", "Rajasthan", "Kerala", "Goa", "Tamil Nadu",
            "Karnataka", "Maharashtra", "West Bengal", "Uttar Pradesh", "Madhya Pradesh",
            "Gujarat", "Punjab", "Jammu & Kashmir", "Ladakh", "Andaman & Nicobar"
        ]
        
        preferred_states = st.multiselect(
            "Select preferred states (optional)",
            state_options,
            help="Leave empty to get recommendations across all India"
        )
    
    # Get AI Recommendations Button
    if st.button("🚀 Get AI Recommendations", type="primary"):
        if not name:
            st.error("Please enter your name")
            return
        
        if not interests:
            st.error("Please select at least one interest")
            return
        
        # Create user profile
        user_profile = {
            'name': name,
            'age': age,
            'budget': budget,
            'duration': duration,
            'interests': interests,
            'states': preferred_states,
            'travel_style': travel_style,
            'group_size': group_size,
            'season': season
        }
        
        # Show AI processing
        with st.spinner("🤖 Llama 3.2 is analyzing your preferences and generating personalized recommendations..."):
            ai_response = call_llama_api(user_profile)
        
        try:
            # Parse AI response
            recommendations_data = json.loads(ai_response)
            
            # Display AI-powered recommendations
            st.markdown("---")
            st.markdown("## 🤖 AI-Personalized Recommendations")
            
            # AI Analysis Card
            st.markdown("""
            <div class="ai-card">
                <h3>🧠 AI Analysis Complete!</h3>
                <p>Llama 3.2 has analyzed your profile and generated personalized recommendations based on your preferences, budget, and travel style.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display recommendations
            if recommendations_data.get('recommendations'):
                for i, rec in enumerate(recommendations_data['recommendations'], 1):
                    st.markdown(f"""
                    <div class="recommendation-card">
                        <h3>{i}. {rec['name']}, {rec['state']}</h3>
                        <p><strong>Why it's perfect for you:</strong> {rec['description']}</p>
                        <p><strong>Best Time to Visit:</strong> {rec['best_time']}</p>
                        <p><strong>Estimated Budget:</strong> {rec['estimated_budget']}</p>
                        <p><strong>Highlights:</strong> {', '.join(rec['highlights'])}</p>
                        <p><strong>AI Relevance Score:</strong> {rec['relevance_score']}/10</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Travel Tips
            if recommendations_data.get('travel_tips'):
                st.markdown("## 💡 AI Travel Tips for You")
                for tip in recommendations_data['travel_tips']:
                    st.markdown(f"• {tip}")
            
            # Hidden Gems
            if recommendations_data.get('hidden_gems'):
                st.markdown("## 💎 AI-Recommended Hidden Gems")
                for gem in recommendations_data['hidden_gems']:
                    st.markdown(f"• {gem}")
            
            # User Profile Summary
            with st.expander("📊 Your Travel Profile Summary"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Name:** {name}")
                    st.markdown(f"**Age Group:** {age}")
                    st.markdown(f"**Budget:** {budget}")
                    st.markdown(f"**Duration:** {duration}")
                
                with col2:
                    st.markdown(f"**Travel Style:** {travel_style}")
                    st.markdown(f"**Group Size:** {group_size}")
                    st.markdown(f"**Season:** {season}")
                    st.markdown(f"**Interests:** {', '.join(interests)}")
                    if preferred_states:
                        st.markdown(f"**Preferred States:** {', '.join(preferred_states)}")
                
                st.markdown(f"**AI Model:** Llama 3.2")
                st.markdown(f"**Recommendations Generated:** {len(recommendations_data.get('recommendations', []))}")
        
        except json.JSONDecodeError:
            st.error("Error parsing AI response. Please try again.")
        except Exception as e:
            st.error(f"Error displaying recommendations: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; font-size: 0.9rem;">
        🤖 Powered by Llama 3.2 AI | 🇮🇳 Discover India with Intelligence
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
