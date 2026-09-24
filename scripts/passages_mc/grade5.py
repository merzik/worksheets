from passages_mc import passage, question

PASSAGES = [
    passage(
        "One Variable",
        "Amira",
        """
        Amira's lab partner wanted to test plant food and a new pot at the same time. If the plant improved, they would not know which change had caused it. The assignment allowed one variable. Two changes would make the conclusion a guess, and the graph would not be able to support it.

        Amira said they should keep the pot and change only the plant food. Her partner argued that a bigger pot was obviously better. Amira pointed to the worksheet: same light, same water, one difference. They labeled the cups Old food and New food, set them in the same window, and measured the stems every other day. The pots stayed identical.

        After a week the new-food stem was taller by two centimeters. Because nothing else had changed, they could write that the food was the likely cause. Amira added a sentence the partner had not wanted: they still did not know what a bigger pot would do. An honest limit was part of the result.
        """,
        [
            question(
                "What problem does the partner's plan create?",
                "Two changes at once would make the cause unclear.",
                "The worksheet forbids measuring the stems.",
                "The plants are required to use different windows.",
                "A bigger pot is the only variable the lab allows.",
            ),
            question(
                "What do they agree to keep the same?",
                "The pots, the light, and the water",
                "The plant food and the pot size",
                "Nothing, so both ideas can be tested together",
                "The final sentence of the conclusion",
            ),
            question(
                "Why can they claim the food caused the growth?",
                "It was the only difference between the two cups.",
                "The taller plant also had a bigger pot.",
                "Amira's partner said a bigger pot was obviously better.",
                "They skipped the measurements and guessed.",
            ),
        ],
    ),
    passage(
        "The Axis",
        "Noah",
        """
        Noah's conclusion said the plants grew fastest in the shade. His graph showed the opposite. The sunny plants had the taller bars. If he turned the project in that way, he would be arguing against his own data, and a judge would notice before he finished the first sentence.

        He did not change the bars to match the sentence. He read the axis labels again. The vertical axis was centimeters, and he had described the short bars as the winners because he liked the shade hypothesis. The numbers did not agree with that hope. Noah rewrote the conclusion so it followed the bars: the sunny plants grew more.

        He added one line about what the shade plants did instead of pretending they had won. Ms. Patel said the new conclusion was stronger because a reader could check it against the graph. Noah stapled the old sentence to the back of his notes as a reminder not to defend a guess after the data is in.
        """,
        [
            question(
                "What is the conflict in Noah's project?",
                "His conclusion says the opposite of what the graph shows.",
                "The sunny plants have no bars on the graph.",
                "Ms. Patel tells him to hide the measurements.",
                "The vertical axis is labeled with the wrong plant.",
            ),
            question(
                "Why is his first conclusion wrong?",
                "He described the result he hoped for, not the taller bars.",
                "The shade plants really did grow more centimeters.",
                "He changed the bars before he read them.",
                "The graph has no axis labels to check.",
            ),
            question(
                "What makes the revised conclusion stronger?",
                "A reader can check it against the graph.",
                "It still claims the shade plants won.",
                "He removes the graph so the sentence cannot be tested.",
                "Ms. Patel writes the conclusion for him.",
            ),
        ],
    ),
    passage(
        "Before It Is Sent",
        "Jade",
        """
        Jade drafted an email to the custodian about the overflowing recycling bins. The first version sounded like an accusation: You never empty these. Mr. Patel read it and said a person who feels blamed may not help, even when the request is fair. The bins still needed to be emptied. The tone was the part that could fail.

        Jade rewrote the message. She named the problem, the place, and a time: the bins by the gym door were full after lunch, and the club could bag the overflow if a pickup could happen before Friday. She took out the word never. She left in the facts. Mr. Patel asked whether she would want to receive the new version. She would.

        They sent it. The custodian replied that afternoon with a Friday time and a thank-you for the offer to bag the overflow. Jade saved both drafts in her folder. The first one showed her frustration. The second one got the bins emptied.
        """,
        [
            question(
                "What is weak about Jade's first email?",
                "It accuses the custodian instead of stating a clear request.",
                "It forgets to mention that the bins by the gym are full.",
                "Mr. Patel sends it before she can revise.",
                "It offers help and nothing else.",
            ),
            question(
                "What does Jade keep when she revises?",
                "The facts about where the bins are and when they fill up",
                "The word never, because it sounds urgent",
                "The accusation, but she adds a smiley face at the end",
                "Nothing from the first draft at all",
            ),
            question(
                "Why does the second draft work better?",
                "It asks for a pickup and offers help without blaming anyone.",
                "It demands that the custodian apologize first.",
                "It never says where the bins are.",
                "The custodian empties them because Jade sounds angry.",
            ),
        ],
    ),
    passage(
        "Half the Lights",
        "Diego",
        """
        Diego was testing the stage lights for the concert when the breaker tripped. All eight lights had been on at once. The stage went dark, and the clock said they had fifteen minutes before the audience came in. Resetting the breaker and turning every light on again would likely trip it a second time.

        The custodian reset the breaker and told Diego the circuit could not carry the full load. Diego switched on four lights, waited, and then tried a fifth. The fifth was the one that made the breaker hum, so he turned it off. Four lights stayed on. The stage was dimmer than the plan, but it was lit.

        He moved two of the working lights closer to the solo mic so the singer would not stand in a shadow. He labeled the fifth switch Do not use together and told the stage crew. The concert happened under fewer lights. A dark stage would have been worse than a dim one.
        """,
        [
            question(
                "What happens when all eight lights are on?",
                "The breaker trips and the stage goes dark.",
                "The audience arrives early and the concert starts.",
                "The custodian says the circuit can carry the full load.",
                "The solo mic stops working in the bright light.",
            ),
            question(
                "How does Diego find a load the circuit can carry?",
                "He adds lights one at a time until the breaker hums.",
                "He turns all eight on again immediately.",
                "He refuses to reset the breaker.",
                "He leaves the stage dark until the concert ends.",
            ),
            question(
                "What tradeoff does he accept?",
                "A dimmer stage is better than no light at all.",
                "The fifth light must stay on even if it trips the breaker.",
                "The singer should stand in the darkest spot.",
                "The crew should ignore the labeled switch.",
            ),
        ],
    ),
    passage(
        "The Wrong Address",
        "Sofia",
        """
        Sofia's petition asked the city to fix the crosswalk by the school. She had already collected twenty signatures when a parent noticed the address. The form said Fifth and Oak. The dangerous crossing was Fifth and Elm. Signatures on a form with the wrong corner could be set aside, and the city might repair a corner that was not the problem.

        Sofia stopped collecting names. She checked the school's written request and the map by the office. Both said Elm. She did not scribble over the old address, because a marked-up petition looks unofficial. She printed a corrected page, wrote a one-sentence note explaining the change, and asked the twenty signers whether they would sign again.

        Eighteen signed the new page that afternoon. Two said they would sign in the morning. Sofia attached the note so a clerk would see why two versions existed. The petition now named the corner where students actually crossed.
        """,
        [
            question(
                "What is wrong with the petition?",
                "It names Fifth and Oak instead of Fifth and Elm.",
                "The city has already repaired the Elm crossing.",
                "Twenty people signed the corrected page first.",
                "The school map shows Oak as the dangerous corner.",
            ),
            question(
                "Why doesn't Sofia just cross out the old address?",
                "A marked-up petition can look unofficial.",
                "The parent tells her Oak is the right corner.",
                "She has not collected any signatures yet.",
                "The clerk asked her to keep the mistake.",
            ),
            question(
                "How does she make the petition usable?",
                "She prints a corrected page and asks people to sign again.",
                "She submits the Oak address because twenty people signed it.",
                "She removes the note so the two versions are a surprise.",
                "She changes the map to match the mistake.",
            ),
        ],
    ),
    passage(
        "What the Budget Can Carry",
        "Luis",
        """
        The class trip budget was forty dollars short. A student suggested cutting the bus and asking families to drive. That would save money, but it would also leave out anyone whose family could not drive that day. The trip was supposed to include the whole class, not only the students who could find a ride.

        Luis listed the costs on the board: bus, tickets, and decorations for the bus windows. The decorations were the only item that did not change who could go. The group voted to drop them and keep the bus. Luis rewrote the budget, subtracted the decoration price, and checked the sum twice. The new total fit.

        They sent the revised budget to the office with a one-line note: decorations cut so every student can ride. The office approved it the next morning. The bus was less colorful. It was also full.
        """,
        [
            question(
                "Why is cutting the bus a poor solution?",
                "Some students would be left out if families had to drive.",
                "The decorations cost more than the bus.",
                "The office has already canceled the tickets and the bus.",
                "Luis wants only part of the class to attend.",
            ),
            question(
                "What do they cut instead?",
                "The decorations, which do not decide who can go",
                "The tickets, so the bus can be more colorful",
                "The note to the office",
                "Half the class from the trip list",
            ),
            question(
                "What does the revised budget protect?",
                "A seat on the bus for every student",
                "The window decorations",
                "A plan that depends on family cars",
                "A total that still does not fit",
            ),
        ],
    ),
    passage(
        "Not Everyone",
        "Noor",
        """
        Noor's article said everyone in the school wanted a longer recess. Her evidence was a survey of her own class. Twenty-two students had voted yes. That was a real result. It was not a result about the whole school. A reader who trusted the headline would believe something the survey had never asked.

        Mr. Patel circled the word everyone. Noor replaced it with "our class" and added the number twenty-two. She did not hide that the survey was small. She wrote one more sentence: other grades have not voted yet. The claim was now the size of the evidence.

        The article ran that way. Two students from another grade asked how they could take the same survey. Noor kept the crossed-out draft because it showed the difference between a wish and a count. A bigger claim would have needed a bigger survey.
        """,
        [
            question(
                "What is overstated in Noor's first draft?",
                "She says the whole school wants something only her class voted on.",
                "She hides the fact that twenty-two students in her class voted yes.",
                "Mr. Patel tells her to make the claim larger.",
                "The survey included every grade.",
            ),
            question(
                "How does she make the claim match the evidence?",
                "She names her class and the number of votes.",
                "She deletes the survey so the headline can stay.",
                "She changes the votes from yes to no.",
                "She surveys the school and keeps the word everyone.",
            ),
            question(
                "What does the crossed-out draft remind her?",
                "A bigger claim needs a bigger survey.",
                "Headlines should always say everyone.",
                "Numbers make an article less honest.",
                "Other grades are not allowed to vote.",
            ),
        ],
    ),
    passage(
        "Swapped Wires",
        "Leo",
        """
        Leo's robot car was supposed to drive toward a black line. It drove away from the line every time. He was about to rewrite the whole program. His notes from last week said the program had worked before the car was rebuilt. If the code had not changed, the new wires were the likely problem.

        He checked the diagram taped inside the lid. The left sensor wire was on the right port. Leo swapped those two wires and changed nothing in the program. He put the car at the start of the tape line. It twitched, corrected, and followed the line to the end.

        Leo labeled the ports with a marker so the next rebuild would match the diagram. He also wrote in his log that he had tested one change at a time. Rewriting the program first would have hidden a wiring mistake under a pile of new code.
        """,
        [
            question(
                "What does the car do wrong?",
                "It drives away from the line it should follow.",
                "It follows the line, so Leo rewrites the program anyway.",
                "The diagram shows the wires were already correct.",
                "The sensors work only after the code is deleted.",
            ),
            question(
                "Why doesn't Leo rewrite the program first?",
                "The same program worked before the car was rebuilt.",
                "The wires match the diagram exactly.",
                "He wants to change the code and the wires together.",
                "The car already follows the line.",
            ),
            question(
                "What single change fixes the car?",
                "He swaps the two sensor wires.",
                "He deletes the program and starts over.",
                "He removes the black line from the floor.",
                "He labels the ports and leaves the wires crossed.",
            ),
        ],
    ),
    passage(
        "Two Dates",
        "Felix",
        """
        Felix's report said the town library opened in 1912. A website said 1920. Both could not be the year of the opening. If he picked the date he liked better, the report would depend on a preference instead of a source a reader could check.

        He turned to the town history in the school library, the book his teacher had named as the reference. The index listed the opening under 1920, with a photograph and a caption. The website did not say where its date came from. Felix changed his sentence to 1920 and cited the book. He mentioned the website in a note: an online page says 1912 but gives no source.

        His teacher said the note was the important part. Felix had not pretended the conflict was invisible. He had shown which source he trusted and why. A reader who disagreed could look at the same page.
        """,
        [
            question(
                "What problem does Felix find in his research?",
                "Two sources give different years for the library opening.",
                "The school library has no history of the town.",
                "The photograph proves the website's date.",
                "His teacher tells him to pick the year he likes.",
            ),
            question(
                "Why does he trust the book more than the website?",
                "The book is the assigned reference and shows where the date comes from.",
                "The website explains its date with a captioned photograph and a citation.",
                "1912 appears in both sources.",
                "The book never mentions the library.",
            ),
            question(
                "What does the note at the end accomplish?",
                "It shows the conflict instead of hiding it.",
                "It erases the book from the report.",
                "It claims both years are equally sourced.",
                "It tells readers not to check the page.",
            ),
        ],
    ),
    passage(
        "The Buzz in the Take",
        "Nina",
        """
        The choir's recording of the third song had a buzz under the voices. Nina traced it to a phone that had been left against the speaker. They could release the take, buzz and all, or record the song again and lose the rest of the rehearsal. The other three songs were clean. Only one track was the problem.

        Mr. Ellis said they did not need to redo the whole concert. They would rerecord the third song from the second verse, where the buzz began, and keep the clean opening. Nina moved the phone across the room. She also checked that no one else had a device near the speaker. They sang the section twice. The second take was quiet underneath.

        She labeled the files so the editor would join the clean opening to the new section and delete the buzz. The recording was not one perfect take. It was a careful splice. Listeners would hear the choir, not the phone.
        """,
        [
            question(
                "What is wrong with the recording?",
                "A phone against the speaker adds a buzz to one song.",
                "All four songs are too quiet to use.",
                "Mr. Ellis wants the buzz left in on purpose.",
                "Nina deletes the clean opening.",
            ),
            question(
                "Why don't they rerecord the entire concert?",
                "Only the third song is damaged, and the opening of it is clean.",
                "The phone cannot be moved.",
                "The other songs have the same buzz.",
                "There is no time left to sing even one short section of the song.",
            ),
            question(
                "What does Nina's file label protect?",
                "The edit that joins the clean opening to the new section",
                "The buzz, so listeners can still hear the phone in the song",
                "A plan to throw out every song",
                "The phone's place against the speaker",
            ),
        ],
    ),
    passage(
        "Double the Salt",
        "Sam",
        """
        Sam was scaling Grandma's soup for the class lunch. The recipe served four. He needed enough for twenty-four, so he multiplied by six. He did that for every line, including the salt. When he tasted a spoon of the broth, it was too salty to serve. Multiplying the salt the same way as the water had been the mistake. Salt does not have to grow as fast as the pot.

        He could not un-salt the pot. He set that broth aside for a bean dish that could use the extra, and he started a second pot. This time he multiplied the water, beans, and vegetables by six, and the salt by three. He wrote the new amounts in a column beside the original card before he measured.

        The second pot tasted like Grandma's, only larger. Sam labeled the salty pot so nobody would ladle it out as the main soup. Scaling a recipe, he wrote on the card, is not the same as multiplying every line.
        """,
        [
            question(
                "Why is the first pot too salty?",
                "Sam multiplied the salt by the same number as the water.",
                "The recipe already served twenty-four people.",
                "He forgot to add any salt at all.",
                "Grandma's card says salt should be doubled every time.",
            ),
            question(
                "What does he do with the salty broth?",
                "He saves it for a bean dish and starts a second pot.",
                "He serves it as the class soup anyway.",
                "He multiplies the salt by six again.",
                "He pours it out and keeps no note of the mistake.",
            ),
            question(
                "What rule does he add to the card?",
                "Scaling a recipe is not the same as multiplying every line.",
                "Always multiply salt by more than the water.",
                "Never write the new amounts beside the original recipe card.",
                "A salty pot should be the main dish.",
            ),
        ],
    ),
    passage(
        "One Square Off",
        "Hana",
        """
        Hana's mural group had painted the sky before they checked the grid. The tree on the wall sat one square to the left of the tree on the sketch. If they kept painting, the doorway in the mural would not line up with the real doorway it was supposed to frame. Wet paint could still be wiped. Dry paint would have to be covered.

        They stopped and held the sketch against the wall. The pencil grid on the wall had been started from the wrong edge. Hana wiped the wet tree back to bare primer. She remarked the squares from the doorway outward, the way the sketch was measured, and only then redrew the tree. The rest of the mural waited.

        The tree landed on the same square as the sketch. They let that section dry before they opened the other paints. Hana wrote on the sketch: measure from the doorway, not from the left edge. One wrong starting point had moved everything.
        """,
        [
            question(
                "What is wrong with the mural?",
                "The tree is one square left of where the sketch places it.",
                "The doorway in the room has been moved.",
                "The sketch has no grid to compare.",
                "Dry paint is covering a tree that is already correct.",
            ),
            question(
                "Why do they wipe the tree instead of painting over it later?",
                "The paint is still wet, so it can come off the primer.",
                "The sketch is wrong and the wall is right.",
                "They want the doorway in the mural to miss the real one.",
                "The grid was measured from the doorway already.",
            ),
            question(
                "What starting point fixes the grid?",
                "Measuring from the doorway outward",
                "Measuring from the left edge again",
                "Painting the rest of the mural before checking",
                "Ignoring the sketch once the sky is done",
            ),
        ],
    ),
    passage(
        "More Than Praise",
        "Andre",
        """
        Andre's peer review of Lila's story said only "This is great." Lila asked which part was great. Andre could not point to a sentence. The review felt kind, and it gave her nothing to revise. Their teacher had asked for one strength and one specific suggestion. Praise alone did not meet the assignment.

        Andre read the story again with a pencil. The opening put the reader in the rain with the character. That was the strength, and he named the sentence. The ending solved the problem in one line, so fast that he did not see how the character decided. He wrote: show the choice in two more sentences, and he quoted the line that rushed past it.

        Lila used the note. The new ending kept the same solution and added the moment of choosing. Andre's second review was shorter on praise and more useful. Kindness, he decided, included telling a writer what to try next.
        """,
        [
            question(
                "What is missing from Andre's first review?",
                "A specific suggestion Lila can use",
                "Any kind word at all",
                "The story he was supposed to read",
                "The teacher's request for praise only",
            ),
            question(
                "What strength does he name the second time?",
                "The opening that puts the reader in the rain",
                "The ending that explains every choice slowly",
                "A sentence he never actually read",
                "The fact that the story needs no changes",
            ),
            question(
                "How does Lila use his suggestion?",
                "She keeps the solution and adds the moment of choosing.",
                "She deletes the opening he liked.",
                "She ignores the note and leaves the rushed line.",
                "She asks him to write the ending for her.",
            ),
        ],
    ),
    passage(
        "The Missing Hour",
        "Mei",
        """
        Mei's weather graph had a smooth line through Tuesday afternoon, but the log had no number for 2:00. She had been at a rehearsal. If she drew the line as if the temperature had been measured, the graph would invent data. A gap is not the same as a zero, and it is not the same as a guess.

        She erased the smooth line through that hour. She left a break in the graph and wrote "no reading" under it. Then she checked the hours she had actually recorded and plotted only those. The line stopped, started again at 3:00, and the break was obvious. Anyone looking at the graph could see where the instrument had not been read.

        Mr. Chen said the break was more scientific than a pretty line. Mei added a sentence to her conclusion: Tuesday at 2:00 is unknown. Unknown was an honest word. Filling it in would have made the graph look complete and made it a story she had not measured.
        """,
        [
            question(
                "What is dishonest about the smooth line?",
                "It pretends there was a 2:00 reading when the log has none.",
                "It shows the hours Mei actually measured.",
                "It marks the gap as unknown.",
                "Mr. Chen asked her to invent the missing temperature.",
            ),
            question(
                "How does Mei show the gap?",
                "She breaks the line and writes no reading under that hour.",
                "She writes zero for 2:00.",
                "She copies the 3:00 number into the empty 2:00 space.",
                "She removes Tuesday from the graph entirely.",
            ),
            question(
                "Why is the break more scientific than a pretty line?",
                "It shows what was measured and what was not.",
                "It makes the temperature look steady all afternoon.",
                "It hides the rehearsal so the graph seems complete.",
                "It changes the 3:00 reading to match a guess.",
            ),
        ],
    ),
    passage(
        "Two Lines Too Many",
        "Camila",
        """
        Camila's scene ran a minute longer than the slot the play could give it. The problem was not the plot. Two speeches said the same fact: the key was in the drawer. The second speech did not add a decision or a feeling. It only repeated the information, and the scene missed its cue for the lights.

        She did not cut the moment when the character decides to open the drawer. She cut the repeated sentences and left the decision. Then she read the scene aloud with a timer. It fit the slot with five seconds to spare. Her partner still understood where the key was, because the first speech had said it.

        At rehearsal the lights came up on time. Camila marked the cut in the script so nobody would restore the repeated lines later. Shorter was not the same as thinner. The scene had lost an echo and kept the choice.
        """,
        [
            question(
                "Why is the scene too long?",
                "Two speeches repeat the same fact about the key.",
                "The character never decides to open the drawer.",
                "The timer says the scene is already short enough.",
                "The lights are supposed to come up late.",
            ),
            question(
                "What does Camila refuse to cut?",
                "The moment when the character decides",
                "Both speeches, so the key is never mentioned",
                "The timer, because the slot does not matter",
                "The cue that brings the lights up",
            ),
            question(
                "What does the timed reading show?",
                "The scene fits the slot once the echo is gone.",
                "The partner no longer knows where the key is.",
                "The decision has to be removed too.",
                "The play needs the repeated lines to make sense.",
            ),
        ],
    ),
    passage(
        "Three Steps on the Door",
        "Mateo",
        """
        Students kept bringing found items to the office in different ways. Some left them on the counter with no name. Some carried them from class to class. A glove sat in the lost-and-found for a week because nobody had written where it was found. The office could not return what it could not describe.

        Mateo asked the secretary which three facts she needed. She said: what it is, where it was found, and the date. He made a half-sheet with those three lines and a box for the finder's name, which was optional. He did not ask finders to search the item for money or cards. He posted the sheet by the office door and put a pencil on a string.

        The next found item, a water bottle, came in with the form filled out. The owner claimed it the same day because the form said "gym bench, Tuesday." Mateo left a stack of blank forms in the pocket under the sign. A clear process was faster than a mystery bin.
        """,
        [
            question(
                "Why do found items sit unclaimed?",
                "The office often does not know what they are or where they were found.",
                "The secretary refuses to accept any lost item.",
                "Students already fill out a complete form every single time they visit.",
                "Mateo tells finders to search wallets for cash.",
            ),
            question(
                "What three facts does the form ask for?",
                "What it is, where it was found, and the date",
                "The owner's address, phone number, and password",
                "Only the finder's name",
                "How much money was inside",
            ),
            question(
                "How does the water bottle show that the form works?",
                "The owner finds it the same day because the place and day are written down.",
                "It sits for a week with a blank sheet.",
                "Mateo keeps the bottle because filling out the form is optional for finders.",
                "The gym bench is not mentioned anywhere.",
            ),
        ],
    ),
    passage(
        "The Long Intro",
        "Priya",
        """
        Priya's podcast about the garden club ran nine minutes. Four of those minutes were her introduction. The interview with the club leader was the part listeners had come for, and it was shorter than the welcome. A host who talks more than the guest has buried the story.

        She did not delete the interview to save time. She cut her own opening. The first draft explained the whole history of the garden. The revision said who the guest was, why the club mattered this month, and one question she hoped to answer. That took forty-five seconds. She timed it.

        She played the new cut for two classmates who had not heard the draft. They could retell the guest's main point. They could not retell the old introduction, because it was no longer there. Priya kept the long intro in a folder labeled unused. The episode that went out belonged mostly to the person she had interviewed.
        """,
        [
            question(
                "What is out of balance in the first episode?",
                "Priya's introduction is longer than the interview.",
                "The guest talks for four minutes more than Priya.",
                "Classmates can retell the introduction and not the guest.",
                "The revision adds the whole history of the garden.",
            ),
            question(
                "What does Priya cut?",
                "Her own opening, not the guest's interview",
                "The guest's main point",
                "The timer, so length will not matter",
                "Every question she hoped to answer",
            ),
            question(
                "How does she know the new cut works?",
                "Classmates can retell the guest's point after one listen.",
                "They memorize the unused introduction.",
                "The episode is now mostly her welcome.",
                "She deletes the whole folder of unused introduction audio.",
            ),
        ],
    ),
    passage(
        "The Scale Bar",
        "Rosa",
        """
        Rosa's map made the park look smaller than the school, even though students walked ten minutes to reach it. She had drawn both buildings the same width because they fit the page that way. A map that ignores scale teaches the wrong distance. Someone using it to plan a walk would be late.

        She measured the school on a satellite printout and the park on the same printout. The park was about three school-widths across. Rosa redrew the park at that size and added a scale bar: one centimeter equals one hundred meters. She did not stretch the park just to fill the empty corner of the page.

        A classmate used the bar to estimate the walk and came within a minute of the real time. Rosa wrote the scale on the map in ink so a later copy would not drop it. Fitting the page was no longer more important than telling the truth about distance.
        """,
        [
            question(
                "What is misleading about Rosa's first map?",
                "The park and the school look the same size, but they are not.",
                "The scale bar says one centimeter equals one hundred meters.",
                "A classmate's estimate matches the real walk.",
                "The satellite printout shows the park as smaller than it is.",
            ),
            question(
                "How does she decide the park's new size?",
                "She compares both places on the same printout.",
                "She stretches the park until the page looks full.",
                "She erases the school so only the park remains.",
                "She keeps both buildings the same width.",
            ),
            question(
                "What does the classmate's walk test show?",
                "The scale bar predicts the time closely enough to trust.",
                "The first map was already accurate.",
                "Distance does not matter if the page looks balanced.",
                "The park is smaller than the school after all.",
            ),
        ],
    ),
    passage(
        "One Crowded Hour",
        "Hector",
        """
        Twelve students signed up to clean the park, and all twelve chose 10:00. The other hours on the sheet were blank. At 10:00 they would crowd the same path and run out of bags. At noon the park would be dirty again because nobody had stayed. A signup that piles everyone into one hour is not a schedule.

        Hector did not erase names. He asked each person for a second choice and highlighted the hours that still had room. Four students could move to 11:00, and three could move to noon. Five stayed at 10:00, which was enough to start. He rewrote the sheet so each hour had a job: paths, playground, then bins.

        On Saturday the bags lasted, and the park was still being cleaned at noon. Hector left the revised sheet on the club board. Choice was still allowed. It was no longer allowed to ignore the empty hours.
        """,
        [
            question(
                "What is wrong with the first signup?",
                "Everyone chose the same hour, so the rest of the day is empty.",
                "Nobody wanted to clean the park.",
                "Hector erased the names before he asked anyone for a second choice.",
                "The noon group already had too many people.",
            ),
            question(
                "How does Hector fill the empty hours?",
                "He asks for second choices and moves some students.",
                "He assigns all twelve to noon and cancels 10:00.",
                "He tells five students they cannot help.",
                "He leaves the sheet blank and hopes people spread out.",
            ),
            question(
                "What does the Saturday result show?",
                "The work lasts through noon because the hours are spread out.",
                "The bags run out at 10:00 just as they did in the old plan.",
                "The park is dirty again by noon.",
                "Second choices were ignored.",
            ),
        ],
    ),
    passage(
        "Free Means Paid For",
        "Ivy",
        """
        The student-council poster said Free pizza at the dance. Ivy checked the budget. Pizza for the expected crowd cost more than the council had left after the DJ. Free, on a poster, meant the council would pay. They could not pay. Taking the poster down after people had planned on pizza would feel like a trick.

        Ivy brought the numbers to the meeting. The group did not want to cancel the dance. They wanted the poster to tell the truth. She changed the line to Pizza slices for $1, with a note that the price covered the food. She reprinted the poster before the first one had been up for a full day, and she pulled the old copies.

        Students still came. The pizza money matched the receipt. Ivy kept both poster files. The first one was more exciting. The second one was a promise the council could keep.
        """,
        [
            question(
                "Why is the word free a problem?",
                "The council cannot afford the pizza the poster promises.",
                "Students refuse to attend a dance with food.",
                "The DJ costs nothing and the pizza is already paid.",
                "Ivy wants to cancel the dance.",
            ),
            question(
                "What change makes the poster honest?",
                "It lists a one-dollar price that covers the food.",
                "It still says free and hides the budget.",
                "It removes the dance and keeps the pizza line.",
                "It raises the price without telling anyone.",
            ),
            question(
                "Why does Ivy keep both files?",
                "They show the difference between an exciting line and a promise she can keep.",
                "She plans to hang the free-pizza poster on the walls again after the dance.",
                "The receipt proves the pizza was free.",
                "The old copies are still on the walls.",
            ),
        ],
    ),
    passage(
        "Not a Quote",
        "Lila",
        """
        Lila's article included a sentence she had heard a classmate say in the hall: "This test was unfair." She put the name beside it. The classmate had not known he was being interviewed. A quote needs a person who agreed to be quoted. A hallway complaint is not that agreement.

        Lila did not want to lose the point, which was that several students found the test harder than the review sheet. She deleted the name and the quotation marks. She wrote instead that some students said the test felt harder than the review, and she did not claim those were anyone's exact words. Then she asked three students, including the classmate, whether that sentence was fair. They said it was, as long as no name was attached.

        The article kept the criticism and lost the surprise. Lila added a line to her checklist: no name, no quote, unless the person has agreed. The classmate thanked her the next day.
        """,
        [
            question(
                "What is unfair about the first version of the article?",
                "It names a classmate who never agreed to be quoted.",
                "It hides the fact that the test felt hard.",
                "The classmate asked to have his exact words printed.",
                "Lila invents a complaint nobody made.",
            ),
            question(
                "How does she keep the point without the quote?",
                "She reports the idea in her own words and leaves the name off.",
                "She prints the exact quote and adds two more students' names.",
                "She deletes the whole criticism.",
                "She pretends the words came from the teacher.",
            ),
            question(
                "What rule does she add to her checklist?",
                "Do not name or quote someone who has not agreed.",
                "Always use a hallway comment as a quote.",
                "Never write that a test felt hard.",
                "Attach a name even when the person says no.",
            ),
        ],
    ),
    passage(
        "A Fan Instead of Force",
        "Owen",
        """
        The greenhouse window was painted shut. Owen's group needed air moving across the seedlings, which were damp and spotted. Forcing the window could crack the glass, and a cracked pane would cool the room at night. The paint was not going to give way in one class period.

        Ms. Brooks said they could borrow the shop fan if they aimed it across the bench, not straight at the tender leaves. Owen set it on a crate two meters back and turned it to low. He tied a ribbon to the bench so they could see the air move. The ribbon lifted. The leaves did not flatten.

        They left a sign: Fan on low until the window is freed. The spots on the seedlings dried by the next morning, and the glass was still whole. Owen wrote a work order for the painted window instead of pretending the fan was a permanent fix. Air was the need. Breaking the glass was not the method.
        """,
        [
            question(
                "Why shouldn't the group force the window?",
                "The glass could crack and cool the greenhouse at night.",
                "The seedlings need less air, not more.",
                "The fan is already aimed straight at the leaves.",
                "Ms. Brooks says the spots should stay wet.",
            ),
            question(
                "How do they move air without opening the window?",
                "They run a fan on low, aimed across the bench.",
                "They crack the pane just enough for a breeze.",
                "They point the fan directly at the leaves.",
                "They wait and do nothing until the paint is sanded.",
            ),
            question(
                "Why does Owen still write a work order?",
                "The fan is a temporary fix, not a repaired window.",
                "The ribbon showed that no air was moving.",
                "The glass cracked overnight.",
                "He wants the fan to stay forever.",
            ),
        ],
    ),
    passage(
        "A Way to Stop",
        "Theo",
        """
        Theo's program was supposed to print the club's names once. It printed them without stopping. The loop had no test for the end of the list. He could unplug the computer, which would stop the printing and also lose the file if he had not saved. Panic was not a fix he wanted to repeat.

        He saved the file first. Then he looked at the loop. It said "repeat," and it never asked whether any names were left. Theo added a condition: stop when the next line is blank. He ran it on a three-name test list before he used the real one. The test printed three names and ended.

        The full list printed once and stopped. Theo wrote the condition in a comment above the loop so the next editor would see why it was there. A loop without a stop is not a list. It is a machine that does not know it is finished. Theo tested the stop one more time with the full club list before he closed the file and shut the laptop.
        """,
        [
            question(
                "What is wrong with Theo's loop?",
                "It repeats the names and never checks for the end.",
                "It prints three names and stops too soon.",
                "The comment tells it to run forever.",
                "He tests the full list before he saves.",
            ),
            question(
                "What does he do before he changes the code?",
                "He saves the file so unplugging the computer is unnecessary.",
                "He deletes the list of names.",
                "He runs the full name list with the endless loop still in place.",
                "He adds a comment and no condition.",
            ),
            question(
                "How does the new condition work?",
                "The loop stops when the next line is blank.",
                "The loop stops after it has printed forever.",
                "The test list is supposed to run without ending.",
                "A blank line tells the program to start over.",
            ),
        ],
    ),
    passage(
        "The Front Row Twice",
        "Jordan",
        """
        Jordan's seating chart for the visiting authors put two classes in the front row. Both teachers had replied yes to "row 1" because the form allowed it. Chairs did not allow it. If both classes arrived expecting the front, one class would be standing in the aisle while the author waited.

        He did not write to only one teacher and hope the other would not notice. He measured the row: fourteen chairs. Each class had eighteen students, so neither class fit there alone either. Jordan offered each teacher the front for half the event and the second row for the other half. He sent a revised chart that showed the switch at the midpoint, and he asked both to confirm.

        Both confirmed. On the day of the visit, the classes traded at the break without an argument in the aisle. Jordan kept the old form as an example of a question that had allowed two yes answers. The new form asked for a first choice and a second.
        """,
        [
            question(
                "What conflict is built into the seating form?",
                "It lets two classes both claim the front row.",
                "It tells every class to sit in row 2.",
                "Fourteen chairs are enough for both classes at once.",
                "Neither teacher replies.",
            ),
            question(
                "Why can't Jordan simply give the front row to one class?",
                "Neither class fits in fourteen chairs for the whole event, and both were told yes.",
                "The author canceled the visit.",
                "The second row has no chairs.",
                "Both teachers refuse any seat in the room except a spot in the center aisle.",
            ),
            question(
                "What does the revised plan do?",
                "The classes trade the front row at the break.",
                "Both classes stand for the whole visit.",
                "One teacher is never told about the change.",
                "The old form stays in use because two yes answers are fine.",
            ),
        ],
    ),
    passage(
        "In Her Own Words",
        "Elena",
        """
        Elena's biography of a local inventor had one sentence she loved. It was also a sentence from the library book, copied with the same unusual phrase. Changing a word or two would not make it hers. Her teacher had said that borrowed wording needs quotation marks and a citation, or it needs to be rewritten until the structure is new.

        Elena did not want a quote in the middle of a short report, so she closed the book and said the fact aloud. The inventor had built a safer latch for school doors. She wrote that sentence, then checked the book to be sure the fact was right and the wording was not. The unusual phrase was gone. The fact remained.

        She added the book to her source list anyway, because the fact had come from it even though the sentence had not. Her teacher circled the new sentence and wrote "yours." Elena kept the copied line in her notes, crossed out, so she could see what she had been tempted to keep.
        """,
        [
            question(
                "What is the problem with Elena's favorite sentence?",
                "It copies the book's wording, not just the fact.",
                "The fact about the latch is incorrect.",
                "Her teacher says quotes are never allowed.",
                "The source list already includes a sentence she invented.",
            ),
            question(
                "How does she rewrite it?",
                "She closes the book and states the fact in her own sentence.",
                "She changes one word and keeps the rest.",
                "She deletes the fact so no source is needed.",
                "She pastes the unusual phrase into the source list.",
            ),
            question(
                "Why does the book stay on the source list?",
                "The fact came from the book even after the words changed.",
                "She is still using the book's exact sentence in the report.",
                "Her teacher said sources are optional.",
                "The copied line was never written down.",
            ),
        ],
    ),
    passage(
        "A Team Twice in a Row",
        "Malik",
        """
        Malik's tournament bracket gave the blue team two games before lunch and gave the green team none until the final. He had copied the names in the order they were written on the signup, and the blue team happened to be listed twice in a row. A fair bracket does not reward a place on a list.

        He did not ask the blue team to give up a win they had not played. No games had started. Malik redrew the bracket so that no team played back-to-back unless it had won its way there. He checked each round: every team appeared once before any team appeared twice. The green team now had a first-round game. The blue team still had a path to the final.

        Coaches from both teams looked at the new bracket and agreed. Malik wrote the rule at the top of the page: a first-round spot is not a prize for signing up early. The tournament started with that page, not with the copied list.
        """,
        [
            question(
                "What is unfair about the first bracket?",
                "One team plays twice before another team plays at all.",
                "The green team has already won the final.",
                "The games have already started and cannot be replayed.",
                "The blue team is missing from the signup.",
            ),
            question(
                "What rule does Malik use when he redraws it?",
                "Every team appears once before any team appears twice.",
                "The signup order decides who plays back-to-back.",
                "The blue team must give up a win.",
                "The green team waits until the final.",
            ),
            question(
                "Why can he change the bracket without taking a win away?",
                "No games have been played yet.",
                "Both coaches refuse to look at the page.",
                "The blue team already lost.",
                "The signup list is the official result.",
            ),
        ],
    ),
    passage(
        "A Question the Chapter Can Answer",
        "Amina",
        """
        Amina's discussion question asked why the character forgave the friend. The chapter ended before the forgiveness. Readers could guess, but they could not point to a sentence. Her teacher had asked for a question the chapter could answer. A question about a later chapter would turn the discussion into speculation.

        Amina reread the last three pages. The character does not forgive. She does decide to return the borrowed book. That decision was on the page, with a reason: she did not want the argument to swallow the friendship. Amina replaced her question with "Why does she return the book?" and underlined the sentence that held the reason.

        The group could answer without inventing a scene. One student still wanted to talk about forgiveness. Amina said they could mark it as a prediction, not as a fact from the chapter. The discussion stayed attached to words they could all find.
        """,
        [
            question(
                "Why doesn't Amina's first question work?",
                "The chapter ends before the forgiveness she asks about.",
                "The character returns the book for no reason.",
                "The teacher wants questions about later chapters only.",
                "The group cannot find any sentence in the chapter.",
            ),
            question(
                "What does the chapter actually show?",
                "The character decides to return the book, and it gives a reason.",
                "The character forgives the friend on the chapter's last page.",
                "The borrowed book is never mentioned.",
                "The argument has already ended the friendship.",
            ),
            question(
                "How does the group handle the forgiveness idea?",
                "They may call it a prediction, not a fact from the chapter.",
                "They treat it as something the chapter already stated.",
                "Amina forbids anyone to mention the friend.",
                "They skip the underlined sentence.",
            ),
        ],
    ),
    passage(
        "Where the Fair Should Stand",
        "Ben",
        """
        The book fair was planned for the lawn. Ben's committee liked the space until he checked the weekend forecast and the custodian's note. Rain was likely, and the lawn had no cover. Moving indoors would mean fewer tables. Staying outside could mean soaked books. Either choice had a cost. Pretending both were perfect would not help the principal decide.

        Ben surveyed the volunteers: would they rather have fewer tables under the gym roof, or the full lawn with a plan to move if rain started? Eighteen chose the gym. Six chose the lawn. He did not hide the six. He put both numbers in the recommendation, then explained that wet books would cost more than the tables they would lose.

        The principal approved the gym. Ben posted the tally so the six volunteers could see they had been counted. The fair was smaller and dry. A recommendation that includes the loss is easier to trust than one that only announces the win.
        """,
        [
            question(
                "What decision is the committee facing?",
                "Whether to risk rain on the lawn or accept fewer tables indoors",
                "Whether to cancel the book fair because nobody at all volunteered",
                "Whether to hide the forecast from the principal",
                "Whether wet books are cheaper than dry ones",
            ),
            question(
                "How does Ben use the survey?",
                "He reports both numbers and explains the cost of wet books.",
                "He counts only the eighteen and throws out the six.",
                "He lets the six cancel the indoor plan.",
                "He skips the recommendation and waits.",
            ),
            question(
                "Why does he post the tally?",
                "So the volunteers who disagreed can see they were counted",
                "So the principal will think the vote was unanimous",
                "So the fair can move back to the lawn in the rain",
                "So the six votes disappear from the record",
            ),
        ],
    ),
    passage(
        "What the Caption Can Claim",
        "Omar",
        """
        Omar's museum caption said the fossil was the oldest bird ever found. The card from the museum loan said it was among the oldest bird fossils in their teaching set. Those are different claims. The first one would be false if a visitor knew of an older fossil. The second one was something the card actually supported.

        He wanted the dramatic sentence. His partner read both versions aloud. The dramatic one had no source on the table. The careful one could be checked against the loan card in the same display. Omar rewrote the caption to match the card and moved "oldest ever" into his speaker notes as a question: how would we know? He would ask the audience, not tell them.

        Visitors could read a true sentence and still hear an interesting question. Omar cited the loan card in small print. A caption that promises more than its source is a story. A caption that stays with its source is information.
        """,
        [
            question(
                "What is the difference between the two claims?",
                "Oldest ever is bigger than anything the loan card supports.",
                "The loan card says the fossil is the oldest bird ever found.",
                "The careful caption cannot be checked.",
                "The dramatic sentence quotes the card exactly.",
            ),
            question(
                "Why does Omar drop the dramatic sentence from the caption?",
                "Nothing on the table is a source for that claim.",
                "His partner prefers captions that visitors cannot check.",
                "The loan card uses the same words.",
                "The audience is not allowed to hear questions.",
            ),
            question(
                "What does he do with the bigger idea instead?",
                "He turns it into a question for the audience.",
                "He prints it as a fact in small type.",
                "He removes the loan card from the display.",
                "He asks visitors to ignore the caption.",
            ),
        ],
    ),
    passage(
        "The Trial That Disagreed",
        "Cole",
        """
        Cole and his partner had written two different results for the same ramp trial. One notebook said the car traveled 80 centimeters. The other said 65. They had watched the same run. Averaging the numbers would hide the disagreement and produce a distance nobody had actually recorded. The lab asked for the measured result, not a compromise.

        They set the ramp up again and agreed on the measuring rule before the car rolled: the front of the car, not the back, and the tape read by the person who was not releasing the car. They ran the trial twice. Both watches agreed: 72 centimeters the first time and 74 the second. Cole wrote both numbers and the rule. He crossed out 80 and 65 with a note: unverified, do not graph.

        The graph used 72 and 74. Their teacher said the crossed-out numbers were useful because they showed the group had noticed the conflict. A clean graph of a blurry measurement would have looked sure and been wrong.
        """,
        [
            question(
                "Why is averaging 80 and 65 a bad idea?",
                "It would create a distance neither notebook actually measured.",
                "The lab requires a compromise instead of a measurement.",
                "Both partners already agree on 80.",
                "The ramp cannot be set up again.",
            ),
            question(
                "What do they agree on before they rerun the trial?",
                "Where to measure the car, and who reads the tape",
                "To graph 80 because it is the larger number",
                "To keep the unverified numbers in the graph",
                "To let the person who releases the car also read the tape",
            ),
            question(
                "Why are the crossed-out numbers still useful?",
                "They show the group noticed a conflict instead of hiding it.",
                "They are the numbers that appear on the graph.",
                "They prove the first measurement was exact.",
                "The teacher says a blurry number should be made to look sure.",
            ),
        ],
    ),
]
