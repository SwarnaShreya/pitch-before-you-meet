import re
import streamlit as st

st.set_page_config(
    page_title="Pitch Before You Meet",
    page_icon="🎤"
)

# Each audience has a tailored introduction and conversation prompts.
GUIDES = {
    "Company recruiter": {
        "pitch": [
            "Hi, I'm {name}, a [program] student at Ohio State.",
            "My background is in [field or type of work].",
            "In a recent [role or project], I [contribution and result].",
            "I'm interested in [role] because [reason].",
            "What do you look for in candidates for that kind of role?"
        ],
        "starters": [
            "What roles are you speaking with students about today?",
            "What do you enjoy most about working at your company?",
            "What skills help new hires succeed?"
        ],
        "followup": "What is a good way for a student to demonstrate that?",
        "closing": (
            "Thank you for your guidance. "
            "What would you recommend as my next step?"
        )
    },
    "Hiring manager": {
        "pitch": [
            "Hi, I'm {name}, and I'm studying [program] at Ohio State.",
            "I've worked on [relevant type of work].",
            "One example is [specific contribution and result].",
            "I'd like to apply that experience to [role or business problem].",
            "What would you want someone in this role to accomplish first?"
        ],
        "starters": [
            "What is your team focused on right now?",
            "How does this role collaborate with other teams?",
            "What makes someone effective on your team?"
        ],
        "followup": "How would you measure success in that work?",
        "closing": (
            "I appreciate learning more about your team. "
            "May I follow up with an example of relevant work?"
        )
    },
    "OSU / Fisher alumnus": {
        "pitch": [
            "Hi, I'm {name}, a current [program] student at Ohio State.",
            "It's lovely to meet someone who has been through the program.",
            "Before coming here, I [brief background].",
            "I'm now exploring [career interest].",
            "How did you decide on your direction after graduation?"
        ],
        "starters": [
            "What is a favorite memory from your time at Ohio State?",
            "What experience helped you most after graduation?",
            "What do you wish you had explored more as a student?"
        ],
        "followup": "What made that experience especially useful?",
        "closing": (
            "I enjoyed hearing about your experience. "
            "Would you be comfortable connecting on LinkedIn?"
        )
    },
    "Professor / researcher": {
        "pitch": [
            "Hello Professor [last name], I'm {name}.",
            "I'm studying [program] at Ohio State.",
            "I've been exploring [topic] through [class or project].",
            "Your work on [specific subject] caught my interest.",
            "What would you recommend exploring to understand it better?"
        ],
        "starters": [
            "What first drew you to this research area?",
            "What question are you most curious about right now?",
            "How does this topic connect to practical business problems?"
        ],
        "followup": "What makes that question challenging to study?",
        "closing": (
            "Thank you for explaining that. "
            "May I follow up after exploring your recommendation?"
        )
    },
    "Industry professional": {
        "pitch": [
            "Hi, I'm {name}, a [program] student at Ohio State.",
            "My experience so far has been in [background].",
            "I've particularly enjoyed working on [task or project].",
            "I'm curious about building a career in [industry].",
            "What should someone entering the field understand about the work?"
        ],
        "starters": [
            "How did you get started in your field?",
            "What part of your work do you find most interesting?",
            "What changes have affected your day-to-day work?"
        ],
        "followup": "Could you share an example of that?",
        "closing": (
            "Thank you—that gives me a clearer picture of the field. "
            "Would you be open to staying in touch?"
        )
    },
    "Business networking contact": {
        "pitch": [
            "Hi, I'm {name}.",
            "I'm currently studying [program] at Ohio State.",
            "My background is in [field].",
            "I've recently become interested in [topic or activity].",
            "What brought you to this event?"
        ],
        "starters": [
            "Have you attended this event before?",
            "What has been the highlight of the event for you?",
            "What kind of work keeps you busy these days?"
        ],
        "followup": "How did you become interested in that?",
        "closing": (
            "It was lovely meeting you. "
            "Would you like to exchange LinkedIn details?"
        )
    },
    "Startup founder / entrepreneur": {
        "pitch": [
            "Hi, I'm {name}, a [program] student at Ohio State.",
            "I'm interested in how businesses solve [type of problem].",
            "I've worked on [relevant experience or project].",
            "I'd enjoy learning more about what you're building.",
            "What problem originally inspired you to start the company?"
        ],
        "starters": [
            "How did you find your first customers?",
            "What has surprised you about building the business?",
            "What customer feedback has influenced your direction?"
        ],
        "followup": "How did you decide what to change after hearing that?",
        "closing": (
            "I enjoyed learning about your business. "
            "What is the best way to follow your progress?"
        )
    },
    "Senior leader / executive": {
        "pitch": [
            "Hello, I'm {name}, a [program] student at Ohio State.",
            "My background is in [field].",
            "Through [experience], I've become interested in [business topic].",
            "I'm hoping to develop my ability to [specific skill].",
            "What experience most shaped your approach to leadership?"
        ],
        "starters": [
            "What do you look for when developing people on your team?",
            "What skill should early-career professionals practice more?",
            "How do you keep learning as your responsibilities grow?"
        ],
        "followup": "What does that look like in everyday work?",
        "closing": (
            "Thank you for your time. "
            "I especially appreciated your point about [takeaway]."
        )
    },
    "Potential mentor": {
        "pitch": [
            "Hi, I'm {name}, a [program] student at Ohio State.",
            "I've been exploring a career in [field].",
            "My experience with [project or role] sparked that interest.",
            "I'm currently trying to understand [specific question].",
            "What is one step you would suggest I take?"
        ],
        "starters": [
            "Was there a decision that changed your career direction?",
            "How did you identify opportunities that suited you?",
            "What advice has stayed useful throughout your career?"
        ],
        "followup": "How did you put that advice into practice?",
        "closing": (
            "Thank you for the advice. Would it be okay to send "
            "a short update after I put it into practice?"
        )
    },
    "Classmate / fellow student": {
        "pitch": [
            "Hey, I'm {name}.",
            "I'm studying [program] here at Ohio State.",
            "Before this, I [brief background].",
            "Outside class, I enjoy [interest or hobby].",
            "What are you hoping to explore while you're here?"
        ],
        "starters": [
            "Which class or project are you enjoying most?",
            "What did you do before starting your program?",
            "What do you enjoy doing outside class?"
        ],
        "followup": "What got you interested in that?",
        "closing": (
            "It was great getting to know you. "
            "Would you like to grab coffee sometime?"
        )
    },
    "Career advisor / coach": {
        "pitch": [
            "Hi, I'm {name}, a [program] student.",
            "My background includes [experience].",
            "I'm considering roles in [target area].",
            "So far, I've worked on [preparation you've completed].",
            "What would you suggest I prioritize next?"
        ],
        "starters": [
            "How can I make my career goals more specific?",
            "Which part of my experience should I explain more clearly?",
            "How can I explore whether this role suits me?"
        ],
        "followup": "What would a strong first step look like?",
        "closing": (
            "Thank you. I'll work on [specific action]. "
            "When would it be useful to check back in?"
        )
    },
    "Conference speaker / panelist": {
        "pitch": [
            "Hello, I'm {name}, a student at Ohio State.",
            "Thank you for your session on [topic].",
            "Your point about [specific takeaway] caught my attention.",
            "It connects to [class, project, or interest] I've been exploring.",
            "How would you suggest applying that idea in [context]?"
        ],
        "starters": [
            "What led you to explore this topic?",
            "Was there a finding that surprised you?",
            "What do you hope people take away from the session?"
        ],
        "followup": "Is there a resource you recommend for learning more?",
        "closing": (
            "Thank you for the session and for answering my question. "
            "I look forward to exploring this further."
        )
    }
}

# Remember progress during this visit.
if "page" not in st.session_state:
    st.session_state.page = "welcome"

if "name" not in st.session_state:
    st.session_state.name = ""

if "person" not in st.session_state:
    st.session_state.person = "Company recruiter"


def go_to(page):
    st.session_state.page = page
    st.rerun()


st.title("🎤 Pitch Before You Meet")
st.write("Practice your elevator pitch, one conversation at a time.")
st.caption("Independent student project • Not affiliated with Ohio State.")

# PAGE 1
if st.session_state.page == "welcome":
    st.subheader("Welcome, Buckeye 🌰")
    st.caption(
        "This demo checks email format only. "
        "It does not verify your OSU account."
    )

    with st.form("welcome"):
        name = st.text_input("Your name")
        email = st.text_input(
            "Your OSU email",
            placeholder="lastname.#@osu.edu"
        )
        submitted = st.form_submit_button("Continue →")

    if submitted:
        if not name.strip():
            st.error("Please enter your name.")

        elif not re.fullmatch(
            r"[a-z]+(?:[-'][a-z]+)*\.[0-9]+@osu\.edu",
            email.strip().lower()
        ):
            st.error(
                "Use lastname.#@osu.edu, replacing # "
                "with your assigned number."
            )

        else:
            st.session_state.name = name.strip()
            go_to("choose")

# PAGE 2
elif st.session_state.page == "choose":
    st.subheader(f"Hi, {st.session_state.name}! 👋")
    st.write("Who would you like to practice speaking with?")

    options = list(GUIDES)

    person = st.selectbox(
        "Choose a person",
        options,
        index=options.index(st.session_state.person)
    )

    if st.button("Show my pitch guide →"):
        st.session_state.person = person
        go_to("practice")

    if st.button("← Back to welcome"):
        go_to("welcome")

# PAGE 3
elif st.session_state.page == "practice":
    person = st.session_state.person
    guide = GUIDES[person]

    st.subheader(f"Speaking with: {person}")

    st.markdown("### Your five-sentence starting point")
    st.caption(
        "Replace the bracketed details with your own truthful "
        "experiences. Use this as a guide, not a script to memorize."
    )

    for number, sentence in enumerate(guide["pitch"], start=1):
        personalized = sentence.replace(
            "{name}", st.session_state.name
        )
        st.write(f"{number}. {personalized}")

    st.info(
        "Short on time? Use your introduction, one relevant "
        "detail, and a question. Then pause and listen."
    )

    st.markdown("### Keep the conversation going")

    for question in guide["starters"]:
        st.write(f"• {question}")

    st.markdown("### Try a follow-up")
    st.write(guide["followup"])
    st.caption(
        "Choose a follow-up that fits what they actually said."
    )

    st.markdown("### End the conversation warmly")
    st.write(guide["closing"])

    st.divider()

    st.markdown("### Practice aloud")
    st.write(
        "Try saying your introduction without reading every word. "
        "Aim to sound clear, curious, and like yourself."
    )

    with st.expander("Quick self-check"):
        st.write("• Did I clearly introduce myself?")
        st.write("• Did I share one relevant detail?")
        st.write("• Did I ask a question?")
        st.write("• Did I leave space for them to respond?")
    st.divider()
    st.markdown("### ✍️ Practice your answer")
    st.write(
        "Choose a question, write your answer, and get a basic "
        "practice check. Open the sample if you need inspiration."
    )

    practice_questions = {
        "Give your elevator pitch": {
            "sample": (
                "Hi, I'm [name], a [program] student at Ohio State. "
                "My background is in [field], with experience in "
                "[relevant work]. In one project, I [specific action], "
                "which helped [truthful result]. I'm now exploring "
                "[career direction] because [reason]. "
                "I'd love to hear how your team approaches [topic]."
            ),
            "checklist": [
                "I introduced myself and my current background.",
                "I included one relevant example or contribution.",
                "I explained what I am interested in next.",
                "I ended with a relevant question or invitation."
            ]
        },
        "Tell me about yourself": {
            "sample": (
                "I'm currently studying [program] at Ohio State. "
                "Before this, I worked in [field], where I focused on "
                "[responsibility]. One experience I particularly "
                "enjoyed was [example], because it involved [interest "
                "or skill]. That helped me realize I want to explore "
                "[direction]. I'm now looking for opportunities "
                "where I can contribute through [strength]."
            ),
            "checklist": [
                "I explained what I am doing now.",
                "I selected relevant background rather than my full history.",
                "I included a specific example.",
                "I connected my experience to my next step."
            ]
        },
        "Why are you interested in this company?": {
            "sample": (
                "I'm interested in [company] because of [specific "
                "fact you have researched]. That connects with my "
                "interest in [area]. Through [experience], I learned "
                "that I enjoy [relevant work]. I'd like to understand "
                "how I could bring that experience to [team or role] "
                "while developing my skills in [area]."
            ),
            "checklist": [
                "I mentioned a specific company detail I have verified.",
                "I explained why that detail matters to me.",
                "I connected my experience to the company or role.",
                "I avoided praise that could apply to any company."
            ]
        },
        "What kind of opportunity are you looking for?": {
            "sample": (
                "I'm exploring [role type] in [industry or function]. "
                "I'm especially interested in work involving "
                "[tasks or problems]. My experience with [example] "
                "has given me a foundation in [skills]. I'd like "
                "an opportunity where I can contribute through "
                "[strength] and continue developing [skill]."
            ),
            "checklist": [
                "I named a role, function, or direction.",
                "I described the work I would enjoy doing.",
                "I explained what I can contribute.",
                "I identified something I want to develop."
            ]
        },
        "What is one of your strengths?": {
            "sample": (
                "One of my strengths is [specific strength]. "
                "For example, during [situation], I needed to "
                "[task]. I [specific action], which led to "
                "[truthful outcome]. That experience showed me "
                "how this strength helps with [relevant work]."
            ),
            "checklist": [
                "I chose one clear strength.",
                "I gave a concrete example.",
                "I explained my own actions.",
                "I described the outcome without exaggerating."
            ]
        },
        "Tell me about a challenge you handled": {
            "sample": (
                "During [situation], we faced [challenge]. "
                "My responsibility was to [task]. I first "
                "[action], then [action]. The outcome was "
                "[truthful result]. I learned [lesson], which "
                "I would apply by [future approach]."
            ),
            "checklist": [
                "I briefly explained the situation and challenge.",
                "I made my responsibility clear.",
                "I described what I personally did.",
                "I included the result and what I learned."
            ]
        },
        "Why did you choose your program?": {
            "sample": (
                "I chose [program] because I wanted to develop "
                "[knowledge or skill]. My experience in [background] "
                "made me curious about [topic]. I was particularly "
                "interested in [real feature of the program]. "
                "Through [class or project], I'm now exploring "
                "how to apply that learning to [goal]."
            ),
            "checklist": [
                "I explained my personal reason.",
                "I connected it to my background or goals.",
                "I mentioned a real program feature.",
                "I explained what I hope to do with the learning."
            ]
        },
        "What would you like advice on?": {
            "sample": (
                "I'm exploring [career direction] and trying to "
                "understand [specific question]. So far, I've "
                "[preparation already completed]. I'm deciding "
                "between [options] or considering [next step]. "
                "Based on your experience, what would you "
                "recommend I investigate first?"
            ),
            "checklist": [
                "I gave enough context to understand my question.",
                "I mentioned what I have already tried.",
                "I asked something specific.",
                "I kept the request manageable."
            ]
        }
    }

    question = st.selectbox(
        "What would you like to practice?",
        list(practice_questions),
        key="practice_question"
    )

    exercise = practice_questions[question]

    with st.expander("💡 Show a sample answer"):
        st.write(exercise["sample"])
        st.caption(
            "This is a template, not a claim about your experience. "
            "Replace every bracketed detail with something true."
        )

    # Keep a separate draft for each audience and question.
    draft_id = f"{person}::{question}"

    if "practice_drafts" not in st.session_state:
        st.session_state.practice_drafts = {}

    with st.form("typed_practice_form"):
        answer = st.text_area(
            "Your answer",
            value=st.session_state.practice_drafts.get(draft_id, ""),
            placeholder="Write your answer in your own words...",
            height=200,
            key=f"answer_{draft_id}"
        )

        target = st.selectbox(
            "Target speaking time",
            [30, 60, 90],
            index=1,
            format_func=lambda seconds: f"{seconds} seconds"
        )

        st.write("After writing, review your answer:")
        checked_items = []

        for index, item in enumerate(exercise["checklist"]):
            checked_items.append(
                st.checkbox(
                    item,
                    key=f"review_{draft_id}_{index}"
                )
            )

        check_answer = st.form_submit_button("Check my practice →")

    if check_answer:
        st.session_state.practice_drafts[draft_id] = answer

        if not answer.strip():
            st.warning("Write your answer first, then click Check.")
        else:
            words = len(answer.split())
            estimated_seconds = round(words / 130 * 60)

            left, right = st.columns(2)
            left.metric("Word count", words)
            right.metric(
                "Estimated speaking time",
                f"{estimated_seconds} seconds"
            )

            st.caption(
                "Estimated at 130 words per minute. "
                "Your actual pace and pauses will vary."
            )

            st.markdown("#### Your practice check")

            if re.search(r"\[[^\]]+\]", answer):
                st.warning(
                    "You still have bracketed placeholders. "
                    "Replace them with your own details."
                )

            if estimated_seconds > target:
                st.info(
                    f"This may exceed your {target}-second target. "
                    "Try removing repeated background and keeping "
                    "one strong example."
                )
            elif estimated_seconds < target * 0.5:
                st.info(
                    "You have room to add a relevant detail if needed. "
                    "A short answer is fine when it covers your point."
                )
            else:
                st.success(
                    "The estimated length fits your selected target."
                )

            if words > 0:
                sentences = [
                    part.strip()
                    for part in re.split(r"[.!?]+", answer)
                    if part.strip()
                ]

                if any(
                    len(sentence.split()) > 35
                    for sentence in sentences
                ):
                    st.info(
                        "One sentence is quite long. Try splitting "
                        "it into two so it is easier to say aloud."
                    )

            if (
                question == "Give your elevator pitch"
                and "?" not in answer
            ):
                st.info(
                    "Consider ending with a question that invites "
                    "the other person to respond."
                )

            missing_items = [
                item
                for item, checked in zip(
                    exercise["checklist"], checked_items
                )
                if not checked
            ]

            if missing_items:
                st.write("**Based on your self-check, revisit:**")
                for item in missing_items:
                    st.write(f"• {item}")
            else:
                st.success(
                    "You marked all four self-check items complete. "
                    "Now try saying your answer aloud."
                )

            st.caption(
                "This is a basic rule-based check, not an AI review "
                "or a score. It cannot judge accuracy, relevance, "
                "confidence, or whether your examples are convincing."
            )

    saved_answer = st.session_state.practice_drafts.get(draft_id, "")

    if saved_answer.strip():
        st.download_button(
            "Download my saved answer",
            data=f"{question}\n\n{saved_answer}",
            file_name="practice-answer.txt",
            mime="text/plain",
            key="download_practice"
        )
        st.caption(
            "Click Check again after editing to update the saved answer. "
            "Download it to keep a copy beyond this browser session."
        )

    if st.button("← Choose a different person"):
        go_to("choose")