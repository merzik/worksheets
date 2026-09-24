from passages_mc import passage, question

PASSAGES = [
    passage(
        "The Red Mitten",
        "Mia",
        """
        Mia had to catch the bus, but one red mitten was lost. The morning air was cold, and her bare fingers stung. She looked in both coat pockets. They were empty. She even shook the coat, but nothing fell out.

        She got on her knees and looked under the bed. She found a dusty sock, but not the mitten. Next she dug through her backpack. She found a book and a snack. The mitten was still missing, and she could hear the bus on the street.

        Mom came in and lifted the blanket. The red mitten was lying on the sheet. Mia pulled it on and zipped her coat. She ran outside and got on the bus just in time. She waved to Mom from her seat.
        """,
        [
            question(
                "What is Mia's problem?",
                "One red mitten is lost before the bus comes.",
                "The bus leaves before Mom wakes up.",
                "Her coat pocket has a hole in it.",
                "Her snack is crushed in her backpack.",
            ),
            question(
                "Where does Mia look right after she checks her coat?",
                "She looks under the bed.",
                "She looks in the kitchen sink.",
                "She looks on the bus seat.",
                "She looks in the classroom.",
            ),
            question(
                "How does Mia get her mitten back?",
                "Mom finds it under the blanket.",
                "It falls out when she shakes her coat.",
                "She finds it in her backpack.",
                "A friend on the bus gives her one.",
            ),
        ],
    ),
    passage(
        "Paint on the Rug",
        "Leo",
        """
        Leo was painting a red barn when his cup tipped. Red paint spilled on the classroom rug. The spot grew while he watched. He did not want the rug to stay red.

        First he pressed a dry paper towel on the spot. The smear got bigger, so he stopped rubbing. Next he got a wet rag from the sink. He blotted the paint up instead of scrubbing it across the rug.

        The red spot faded to a light pink. Leo told his teacher what had happened. They moved the paint cups away from the edge of the table. Leo finished his barn with the cup in a safe spot.
        """,
        [
            question(
                "What goes wrong while Leo paints?",
                "Red paint spills on the classroom rug.",
                "Leo cannot find a red crayon.",
                "The barn picture blows off the table.",
                "The sink will not turn on.",
            ),
            question(
                "What happens when Leo uses a dry towel?",
                "The paint smear gets bigger.",
                "The rug turns white again.",
                "The towel soaks up every drop.",
                "The teacher takes the painting home.",
            ),
            question(
                "What finally cleans most of the paint?",
                "Leo blots the spot with a wet rag.",
                "Leo rubs harder with the dry towel.",
                "He paints the whole rug red.",
                "He hides the spot under a chair.",
            ),
        ],
    ),
    passage(
        "The Quiet Puppy",
        "Nora",
        """
        Nora's puppy, Pip, crawled under the porch and would not come out. Rain was starting, and Nora wanted him inside. She called his name three times. Pip stayed in the dark and did not even wag his tail.

        Nora sat on the step and waited so she would not scare him. Then she set a small treat on the walk, a little way from the porch. She patted her knee and spoke in a soft voice. She did not grab for him.

        Pip crept out, ate the treat, and let Nora clip on his leash. They went inside together before the rain got hard. Nora dried his paws with a towel. Pip curled up on his bed.
        """,
        [
            question(
                "What is Nora's problem?",
                "Pip will not come out from under the porch.",
                "Pip ate a treat that was not for him.",
                "The leash is lost in the rain.",
                "Pip will not sleep in his bed.",
            ),
            question(
                "What does Nora do after calling Pip?",
                "She sits and waits, then sets out a treat.",
                "She crawls under the porch and pulls him.",
                "She runs inside and shuts the door.",
                "She asks a neighbor to lift the porch.",
            ),
            question(
                "How does the story end?",
                "Pip comes out and goes inside with Nora.",
                "Pip stays under the porch all night.",
                "The treat rolls away in the rain.",
                "Nora leaves Pip outside with no leash.",
            ),
        ],
    ),
    passage(
        "One Missing Shoe",
        "Owen",
        """
        Owen had one shoe on and one shoe missing. School started soon, and Dad was by the door. Owen looked through the closet. He saw boots and sandals, but not the blue shoe.

        Next he checked the stairs. He found a sock, but the shoe was not there. Then he heard his little sister giggle in the living room. She was feeding her doll. The blue shoe was in the toy box, next to a block.

        Owen lifted it out and said thank you. He put the shoe on and tied it. Dad held the door, and they walked to school together. Owen was not late. His sister waved from the window.
        """,
        [
            question(
                "What is Owen missing?",
                "One blue shoe",
                "His backpack",
                "The house key",
                "Dad's car",
            ),
            question(
                "Where does Owen look before he hears his sister?",
                "In the closet and on the stairs",
                "On the bus and in the gym",
                "Under the sink and in the car",
                "At school and on the playground",
            ),
            question(
                "How is the problem solved?",
                "He finds the shoe in the toy box.",
                "Dad buys him a new pair of shoes.",
                "He wears sandals to school instead.",
                "His sister hides the shoe again.",
            ),
        ],
    ),
    passage(
        "Kite in the Bush",
        "Jade",
        """
        Jade was flying a yellow kite when the wind dropped it into a bush. The string tangled in the branches. She tugged, and the kite only tipped sideways. She was afraid the paper would rip.

        Her brother, Eli, brought a long light stick from the shed. Jade held the kite so it would not tear. Eli lifted the string up and off the twigs. The loop slid free, and the kite came down into Jade's hands.

        They walked to the open field, away from the bushes. Jade let the string out slowly. The kite rose and stayed in the clear sky. She kept her eyes on the branches this time.
        """,
        [
            question(
                "What is Jade's problem?",
                "Her kite is stuck in a bush.",
                "Her kite string is too short.",
                "Eli will not come to the park.",
                "The field is closed for the day.",
            ),
            question(
                "What happens when Jade tugs the string?",
                "The kite tips but stays stuck.",
                "The kite flies higher than before.",
                "The string comes off the kite.",
                "The bush falls over on the path.",
            ),
            question(
                "How do they free the kite?",
                "Eli lifts the string with a stick.",
                "Jade pulls until the branch breaks.",
                "They leave the kite in the bush.",
                "A strong wind rips it loose.",
            ),
        ],
    ),
    passage(
        "Lunch on the Shelf",
        "Luis",
        """
        At lunch, Luis unzipped his backpack and did not see his lunch bag. His stomach growled. The cafeteria line was already closed. He checked both side pockets. They held pencils, but no lunch.

        Luis looked in the lost-and-found bin by the office. He saw a blue hat and a library book, but not his bag. Then he remembered the morning. He had set the bag on the classroom shelf when he hung up his coat.

        He hurried back. The lunch bag was on the shelf, behind a stack of folders. Luis carried it to the table and ate. The next day he put his lunch in his backpack before he hung up his coat.
        """,
        [
            question(
                "What is Luis's problem at lunch?",
                "He cannot find his lunch bag.",
                "The cafeteria runs out of milk.",
                "His coat is in the lost-and-found.",
                "He left his pencils on the bus.",
            ),
            question(
                "What does Luis find in the lost-and-found?",
                "A blue hat and a library book",
                "His lunch bag and a folder",
                "A stack of folders and milk",
                "His coat and his backpack",
            ),
            question(
                "Where was the lunch bag?",
                "On the classroom shelf",
                "In a side pocket",
                "On the bus",
                "In the cafeteria line",
            ),
        ],
    ),
    passage(
        "The Short Crayon",
        "Ava",
        """
        Ava wanted to color the sky blue, but her blue crayon was short and broken. She tried to pinch it, and it slipped. She peeled back the paper so she could hold it better. The crayon still snapped in her fingers.

        Her partner, Nico, had two blue crayons in his tin. Ava asked if they could share. Nico said yes and passed her the longer one. Ava colored the top of the sky. Nico colored the part by the trees.

        The sky looked bright and full. Ava set the short crayon in a cup so it would not get lost on the floor. She thanked Nico. They signed both names on the picture.
        """,
        [
            question(
                "Why is it hard for Ava to color the sky?",
                "Her blue crayon is short and keeps snapping.",
                "The class has no paper left.",
                "Nico will not let her use blue.",
                "The sky in the picture is already done.",
            ),
            question(
                "What does Ava try before she asks Nico?",
                "She peels the paper and tries to hold it.",
                "She paints the sky with a brush.",
                "She trades her picture for a new box.",
                "She colors the sky green instead.",
            ),
            question(
                "How do Ava and Nico solve the problem?",
                "They share Nico's longer blue crayon.",
                "They throw the short crayon away.",
                "Ava colors the sky with a marker.",
                "Nico finishes the picture by himself.",
            ),
        ],
    ),
    passage(
        "The Drooping Plant",
        "Ben",
        """
        Ben's bean plant drooped over the side of the pot. The leaves felt soft, and he was afraid it was dying. He pushed a finger into the soil. The soil was dry all the way down.

        Ben gave the plant a small drink of water. He did not flood the pot. Then he saw that the pot sat in a hot, sunny spot all afternoon. He moved it back from the window so the leaves would not bake.

        The next morning the stem stood taller, and the leaves felt firmer. Ben made a small chart that said, Water me. He checked the soil with his finger each day. The plant kept growing.
        """,
        [
            question(
                "What is wrong with Ben's plant?",
                "It is drooping and the soil is dry.",
                "Bugs have eaten every leaf.",
                "The pot is too heavy to lift.",
                "The chart is missing from the room.",
            ),
            question(
                "What does Ben do after he feels the soil?",
                "He gives the plant a small drink.",
                "He puts the plant outside in the rain.",
                "He cuts off the soft leaves.",
                "He hides the pot in a closet.",
            ),
            question(
                "What helps the plant besides water?",
                "Ben moves it back from the hot window.",
                "Ben waters it until the pot floods.",
                "He sets it in a dark closet.",
                "He stops checking the soil.",
            ),
        ],
    ),
    passage(
        "Rain on the Field",
        "Ella",
        """
        Ella's class was ready for soccer, but rain covered the field. Students groaned and stood by the door. Nobody wanted silent reading instead of a game. Ella raised her hand and asked if they could play in the gym.

        Ms. Ortiz said yes, if they used a soft ball and stayed inside the cones. Ella helped carry the cones to the gym floor. She showed her team where the goal would be. They practiced one short pass before the game.

        The soft ball stayed in bounds. Ella passed to a teammate, and the teammate scored. The class cheered. Recess was different, but it was still a game. They put the cones away when the bell rang.
        """,
        [
            question(
                "What problem does the rain cause?",
                "The class cannot play soccer on the field.",
                "The gym is locked for the day.",
                "Ella forgets how to pass the ball.",
                "Ms. Ortiz cancels the whole school day.",
            ),
            question(
                "What does Ella ask Ms. Ortiz?",
                "If the class can play in the gym",
                "If they can go home early",
                "If she can skip recess",
                "If the soft ball can stay outside",
            ),
            question(
                "How does the class solve the problem?",
                "They play a cone game in the gym.",
                "They wait until the rain stops.",
                "They read quietly by the door.",
                "They move the soccer field inside.",
            ),
        ],
    ),
    passage(
        "Book on the Bus",
        "Noah",
        """
        Noah's library book was due, but it was not in his backpack. He remembered reading it on the morning bus and leaving it on the seat. He did not want to lose a book that was not his.

        Noah told the librarian, Ms. Chen. She called the bus barn. The driver looked in the lost box on bus 12 and said the book was there. Noah would not get it until dismissal, so he wrote the title on a card so he would not forget.

        When the bus came, the driver handed Noah the book. Noah checked it in the next morning, right on time. He wrote his name on a paper bookmark and kept it in his pocket for the next book.
        """,
        [
            question(
                "What is Noah's problem?",
                "He left a library book on the bus.",
                "The librarian lost his bookmark.",
                "Bus 12 does not come to school.",
                "He forgot the name of his teacher.",
            ),
            question(
                "Who helps Noah find out where the book is?",
                "Ms. Chen and the bus driver",
                "His friend on the playground",
                "The cook in the cafeteria",
                "A student on a different bus",
            ),
            question(
                "How does the story end?",
                "Noah gets the book back and returns it.",
                "The driver keeps the book on the bus.",
                "Noah pays for a lost bookmark.",
                "Ms. Chen says the book is not due.",
            ),
        ],
    ),
    passage(
        "The Empty Feeder",
        "Rosa",
        """
        Rosa looked out at the yard and saw the bird feeder hanging empty. Chickadees landed, peeked in, and flew off. She had forgotten to fill it after the windy night. The birds would not stay if there was no seed.

        Rosa poured seed into a cup and carried it outside. She filled the feeder up to the line Mom had marked. Then she shut the lid so the seed would not spill. She stepped back to the window and waited.

        In a few minutes the chickadees came back and took turns on the perch. Rosa smiled. She wrote Fill feeder on the fridge list so the feeder would not sit empty again.
        """,
        [
            question(
                "What is the problem at the start?",
                "The bird feeder is empty, so the birds leave.",
                "The chickadees will not share the perch.",
                "Rosa cannot open the back door.",
                "Mom marked the wrong line on the cup.",
            ),
            question(
                "What does Rosa do with the seed?",
                "She fills the feeder up to Mom's line.",
                "She scatters it all on the grass.",
                "She hides the cup in the fridge.",
                "She feeds it to the chickadees by hand.",
            ),
            question(
                "How does Rosa keep the problem from happening again?",
                "She writes a reminder on the fridge list.",
                "She takes the feeder down for good.",
                "She closes the window so birds cannot see.",
                "She asks the birds to come back tomorrow.",
            ),
        ],
    ),
    passage(
        "The Lost Balloon",
        "Theo",
        """
        Theo's red balloon slipped off his wrist and rose to the ceiling. It stuck there, too high to reach. He jumped three times. His fingers did not even touch the string. He did not want the balloon to pop.

        Theo got a broom from the kitchen. He stood on the rug and tapped the balloon gently. The first tap missed. The second tap pushed the balloon toward the wall. It slid down, and Theo caught the string.

        He tied the string around his wrist in a tight bow. The balloon bobbed beside him, but it could not get away. Theo grinned and showed Mom. Next time he would tie it before he walked inside.
        """,
        [
            question(
                "What is Theo's problem?",
                "His balloon is stuck on the ceiling.",
                "His broom is lost in the kitchen.",
                "The balloon pops in his hands.",
                "Mom says he cannot have a balloon.",
            ),
            question(
                "What happens the first time Theo jumps?",
                "He cannot reach the string.",
                "He knocks the balloon down.",
                "The balloon pops on the light.",
                "Mom lifts him up to the ceiling.",
            ),
            question(
                "How does Theo get the balloon down?",
                "He taps it gently with a broom.",
                "He waits for it to lose all its air.",
                "He climbs on a tall chair.",
                "He pulls the string until it breaks.",
            ),
        ],
    ),
    passage(
        "The Last Piece",
        "Mina",
        """
        Mina was almost done with a puzzle of a red barn. One piece was missing. She looked under the table and found only crumbs. She checked the box lid. The lid was empty. The barn still had a hole in the door.

        Her dog, Buddy, was lying on a blanket nearby. Mina lifted the edge of the blanket. The missing piece was stuck to it. She peeled it off carefully so it would not bend.

        The piece clicked into the door. Mina clapped, and Buddy wagged his tail. She gave Buddy a toy to chew so he would leave the puzzle alone. The finished barn stayed on the table.
        """,
        [
            question(
                "What problem does Mina have?",
                "One puzzle piece is missing.",
                "The puzzle is too hard to start.",
                "Buddy ate the whole puzzle.",
                "The table is too small for the barn.",
            ),
            question(
                "Where does Mina look before she checks the blanket?",
                "Under the table and in the box lid",
                "In the yard and on the bus",
                "Under Buddy's toy and in the sink",
                "In her backpack and at school",
            ),
            question(
                "How does the story end?",
                "She finds the piece and finishes the puzzle.",
                "She throws the puzzle away.",
                "Buddy runs off with the last piece.",
                "The piece stays stuck to the blanket.",
            ),
        ],
    ),
    passage(
        "The Soft Tire",
        "Cole",
        """
        Cole wanted to ride his bike to the park, but the front tire was soft. He pushed the pedal. The bike wobbled, and he had to put a foot down. Riding on a soft tire could bend the rim.

        Cole walked the bike home instead of forcing it. Dad brought the pump from the garage. He showed Cole how to fit the hose on the tire. Cole pushed the pump handle down, slow and steady, until the tire felt firm.

        Cole rode to the corner and back. The tire stayed hard, and the bike did not wobble. He thanked Dad and checked the tire with his thumb. Then he rode to the park on the safe bike.
        """,
        [
            question(
                "Why does Cole stop riding at the start?",
                "The front tire is soft and the bike wobbles.",
                "The park gate is locked.",
                "Dad needs the bike for a trip.",
                "The pump hose will not come off the tire.",
            ),
            question(
                "What does Cole do when the bike wobbles?",
                "He walks the bike home.",
                "He rides faster to the park.",
                "He hides the bike in a bush.",
                "He lets the rest of the air out.",
            ),
            question(
                "How is the tire fixed?",
                "Cole pumps it until it feels firm.",
                "Dad buys a brand-new bike.",
                "Cole patches a hole with tape.",
                "They leave the tire soft.",
            ),
        ],
    ),
    passage(
        "Cat on the Shed",
        "Hana",
        """
        Hana's cat, Miso, was on the shed roof, and the sky was getting dark. Hana called her name. Miso looked down but would not jump. Hana did not climb the shed. The roof was too high, and Dad had said to stay off it.

        Hana shook the food bowl so the kibble rattled. Miso meowed but stayed put. Then Hana set the bowl on the shed step, close to the ground. She moved back and waited without grabbing.

        Miso climbed down to the bowl and ate. Hana picked her up and carried her inside. She shut the shed door so Miso could not get on the roof again that night. Miso purred in her arms.
        """,
        [
            question(
                "What is Hana's problem?",
                "Miso is on the shed roof and will not come down.",
                "The food bowl is empty of kibble and water.",
                "Dad is stuck on the shed roof.",
                "Miso will not eat her dinner.",
            ),
            question(
                "Why does Hana stay off the roof?",
                "It is too high, and Dad said to stay off it.",
                "The roof is already full of cats.",
                "She cannot find the shed.",
                "Miso jumps down as soon as Hana calls her.",
            ),
            question(
                "What gets Miso to come down?",
                "Hana sets the food bowl on the step.",
                "Hana climbs up and lifts her.",
                "Dad shakes a stick at the roof.",
                "Miso jumps when Hana shouts.",
            ),
        ],
    ),
    passage(
        "Hat in the Sand",
        "Amir",
        """
        A big gust blew Amir's hat off at the park. The hat tumbled into the sandbox and kept rolling. Amir ran after it, but the wind pushed it farther. Sand stuck to the wet brim.

        His friend Deon stood in front of the hat to block the wind. The hat stopped against Deon's shoe. Amir picked it up. Sand shook off in a little cloud when he flapped it.

        Amir held the brim with one hand so the next gust could not take it. They went back to the game. Deon grinned. Amir said thank you and kept a hand on his hat.
        """,
        [
            question(
                "What happens to Amir's hat?",
                "The wind blows it into the sandbox.",
                "Deon tosses it into a tree.",
                "Amir leaves it at home.",
                "It falls into the pond.",
            ),
            question(
                "How does Deon help?",
                "He blocks the wind so the hat stops.",
                "He buys Amir a new hat.",
                "He hides the hat in his pocket.",
                "He tells Amir to give up.",
            ),
            question(
                "What does Amir do so the hat will not fly off again?",
                "He holds the brim with one hand.",
                "He buries the hat in the sand.",
                "He lets Deon wear it home.",
                "He ties it to the swing.",
            ),
        ],
    ),
    passage(
        "Spilled Milk",
        "Lucy",
        """
        Lucy reached for the cereal and tipped her glass. Milk ran across the table and dripped onto the floor. She gasped and froze. She did not want Mom to slip in it.

        Lucy got a towel from the drawer. She wiped the table first, then the floor, until the milk was gone. The towel was soggy, so she put it in the sink. The floor was safe to walk on again.

        Mom poured a new cup of milk. Lucy held it with two hands and drank at the table. She set the cup back from the edge. Mom thanked her for cleaning the spill so fast.
        """,
        [
            question(
                "What is Lucy's problem?",
                "Milk spills on the table and the floor.",
                "The cereal box is empty.",
                "Mom cannot find a new cup.",
                "The towel is missing from the store.",
            ),
            question(
                "What does Lucy wipe first?",
                "The table",
                "The window",
                "Her shoes",
                "The cereal bowl",
            ),
            question(
                "How does the story end?",
                "Mom pours a new cup, and Lucy drinks it carefully.",
                "Lucy leaves the milk on the floor.",
                "Mom says Lucy cannot have milk again.",
                "The wet towel stays on the table for the rest of the day.",
            ),
        ],
    ),
    passage(
        "Dot Gets Out",
        "Jack",
        """
        Jack was the helper for Dot the hamster. At reading time, a student whispered that Dot was not in the cage. The lid was open. Jack shut the classroom door so Dot could not run into the hall.

        He looked in the reading corner and behind the bookshelf. No hamster. Then he checked the coat cubbies. Dot was curled in a red hood, nibbling a crumb. Jack cupped him in both hands.

        He set Dot back in the cage and snapped the lid shut. He told the teacher, and they added a second clip to the lid. Dot ran on his wheel. Jack checked the clip twice before he sat down.
        """,
        [
            question(
                "What is the problem in the classroom?",
                "Dot the hamster is out of the cage.",
                "The class cannot find a book to read.",
                "Jack's red hood is missing.",
                "The wheel in the cage is broken.",
            ),
            question(
                "What does Jack do first so Dot cannot get away?",
                "He shuts the classroom door.",
                "He opens every window.",
                "He takes the cage to the hall.",
                "He dumps the coats on the floor.",
            ),
            question(
                "How is Dot kept from getting out again?",
                "Jack shuts the lid and they add a second clip.",
                "Dot stays curled in the red hood for the rest of the day.",
                "The class leaves the lid open.",
                "Jack puts Dot in his backpack.",
            ),
        ],
    ),
    passage(
        "Ball in the Mud",
        "Mei",
        """
        Mei kicked the soccer ball, and it rolled into a deep mud puddle. She stepped in to grab it. Her shoe stuck, and mud climbed over the toe. She backed out before her whole foot sank.

        A long stick lay by the fence. Mei used it to roll the ball to the edge of the puddle. She did not have to step in the deep part. The ball came out brown and dripping.

        Mei rinsed the ball at the water fountain until the mud ran off. Then the class played on the dry grass, away from the puddle. Mei laughed when the clean ball bounced. She kept her shoes on the grass.
        """,
        [
            question(
                "What goes wrong with Mei's kick?",
                "The ball rolls into a deep mud puddle.",
                "The ball flies over the school.",
                "The fountain will not turn on.",
                "Her team goes home early.",
            ),
            question(
                "Why does Mei back out of the puddle?",
                "Her shoe sticks and mud covers the toe.",
                "The stick breaks in her hands.",
                "A friend tells her the ball is lost.",
                "The grass is too dry to play on.",
            ),
            question(
                "How does Mei get the ball out?",
                "She rolls it out with a long stick.",
                "She wades into the deep mud.",
                "She leaves it until the puddle dries.",
                "She kicks a different ball instead.",
            ),
        ],
    ),
    passage(
        "The Torn Page",
        "Ivan",
        """
        Ivan turned a page in his library book too fast, and the page ripped. He started to slide the book into his backpack so no one would see. Then he stopped. Hiding it would not fix the page.

        He carried the book to the desk and showed Ms. Ortiz. She nodded and gave him a strip of tape. She showed him how to press the tape on the back of the page, not across the words. Ivan smoothed it with his finger.

        The page held together, and he could still read every line. Ivan checked the book in and said he was sorry. After that he turned pages slowly and carried books with two hands.
        """,
        [
            question(
                "What happens to Ivan's library book?",
                "A page rips when he turns it too fast.",
                "Ms. Ortiz loses it under the desk.",
                "The tape covers all the words.",
                "He finishes it and wants a new one.",
            ),
            question(
                "What does Ivan almost do with the ripped book?",
                "He almost hides it in his backpack.",
                "He almost reads it to the class.",
                "He almost gives it to a friend.",
                "He almost tapes the cover shut.",
            ),
            question(
                "How is the page fixed?",
                "Ms. Ortiz shows him how to tape the back.",
                "Ivan tears the page the rest of the way out.",
                "They throw the book away.",
                "The rip closes by itself.",
            ),
        ],
    ),
    passage(
        "The Stuck Zipper",
        "Ruby",
        """
        Ruby's backpack zipper stuck halfway, and the bus was coming down the street. She yanked the pull. The zipper stuck worse, and her folder was still inside. She could hear the bus brake at the corner.

        Ruby stopped pulling and looked closely. A bit of cloth from a mitten was caught in the teeth. She pinched the cloth and slid it out slowly. The teeth let go. She did not yank again.

        The zipper closed all the way. Ruby swung the backpack on and ran to the stop. She got on the bus before the door shut. That night she pulled the mitten out of the backpack so it could not catch again.
        """,
        [
            question(
                "What is Ruby's problem?",
                "Her backpack zipper is stuck and the bus is coming.",
                "Her folder is still at school.",
                "The bus door will not open.",
                "She cannot find her red mitten anywhere at home.",
            ),
            question(
                "Why does the zipper get worse at first?",
                "Ruby yanks the pull.",
                "The bus driver takes the backpack.",
                "The folder falls out on the street.",
                "The mitten is still in her pocket.",
            ),
            question(
                "How does Ruby free the zipper?",
                "She slides a caught bit of cloth out of the teeth.",
                "She cuts the backpack open.",
                "She leaves the folder at home.",
                "She asks the driver to wait until the next morning.",
            ),
        ],
    ),
    passage(
        "Mixed-Up Seeds",
        "Sam",
        """
        Sam wanted to plant sunflowers, but the seed cups had been mixed up. The packets had no labels. Some seeds were big and striped. Some were tiny and dark. He did not know which ones were sunflowers.

        He looked at the picture cards on the garden wall. The sunflower card showed big striped seeds. The lettuce card showed tiny dark ones. Sam sorted the seeds into two cups. He checked each seed against the cards before he dropped it in.

        He planted the striped seeds in the sunny row and wrote Sunflower on a stick. The tiny seeds went in the shady row. Sam pressed the soil down gently. Now each row had the right seeds.
        """,
        [
            question(
                "What is Sam's problem?",
                "The seed cups are mixed up and have no labels.",
                "The sunny row is full of weeds.",
                "The picture cards fell off the garden wall.",
                "Sunflowers will not grow in soil.",
            ),
            question(
                "How does Sam tell the seeds apart?",
                "He matches them to the picture cards.",
                "He plants them all in one hole.",
                "He asks the seeds which plant they are.",
                "He throws away the striped ones.",
            ),
            question(
                "Where do the sunflower seeds go?",
                "In the sunny row",
                "In the shady row",
                "Back into the mixed cup",
                "On the garden wall",
            ),
        ],
    ),
    passage(
        "A Long Turn",
        "Nina",
        """
        Nina had been on the swing for a long time. A new student, Mateo, stood nearby and watched. He did not ask, but he looked sad. The rule was to share when someone was waiting.

        Nina dragged her feet and slowed the swing. She hopped off and held the chain so it would not twist. She told Mateo he could have a turn, and she showed him how to pump his legs. Then she counted slowly to twenty.

        When she said twenty, Mateo hopped off and gave the swing back. They took turns two more times. Mateo smiled. Nina was glad she had not kept the swing to herself.
        """,
        [
            question(
                "What is the problem on the playground?",
                "Nina has had a long turn, and Mateo is waiting.",
                "The swing chain is broken.",
                "Mateo will not get off the swing for anyone.",
                "Nina does not know how to pump.",
            ),
            question(
                "What does Nina do after she slows the swing?",
                "She gives Mateo a turn and shows him how to pump.",
                "She tells Mateo to find a different swing.",
                "She counts to twenty and stays on.",
                "She walks away and hides.",
            ),
            question(
                "How does the story end?",
                "Nina and Mateo take turns on the swing.",
                "Mateo leaves the playground sad.",
                "Nina keeps the swing for the rest of recess.",
                "The swing is put away for the day.",
            ),
        ],
    ),
    passage(
        "The Fallen Tower",
        "Omar",
        """
        Omar had built a tall block tower. His little brother, Ali, ran past and bumped the table. The tower crashed, and Ali started to cry. Omar felt mad. He almost yelled.

        Omar took a breath instead. He and Ali picked up every block. Omar said they should build a shorter tower with a wide bottom so it would not fall. Ali stacked two blocks. Omar stacked two more beside them.

        The new tower stayed up. Ali set the last block on top and clapped. They left it on the table for Mom to see. Omar was glad he had not yelled. A wide tower was stronger than a tall one.
        """,
        [
            question(
                "What happens to Omar's tower?",
                "Ali bumps the table and the tower falls.",
                "Mom puts the blocks away.",
                "The blocks are too wide to stack.",
                "Ali builds a taller tower alone.",
            ),
            question(
                "What does Omar do instead of yelling?",
                "He takes a breath and picks up the blocks.",
                "He hides the blocks in his room.",
                "He tells Ali to leave the house.",
                "He builds the same tall tower again.",
            ),
            question(
                "Why does the new tower stay up?",
                "It is shorter and has a wide bottom.",
                "Ali holds it with both hands.",
                "Mom glues the blocks together.",
                "They build it on the floor in the hall.",
            ),
        ],
    ),
    passage(
        "Two Left Boots",
        "Tess",
        """
        Rain tapped the windows, and Tess wanted to splash in the puddles. She pulled on her rain boots and stepped outside. Walking felt wrong. She looked down. Both boots were for the left foot. Her toes were squeezed, and she almost tripped.

        Tess sat on the step and pulled the boots off. She went back inside and looked by the door. One right boot was under the bench, next to a ball. She checked the bottoms. Now she had a left and a right.

        Tess put the pair on and walked through the puddles. Her feet fit, and she did not trip. She laughed when water splashed up. Next time she would look at the boots before she went out.
        """,
        [
            question(
                "What is wrong with Tess's boots?",
                "She is wearing two left boots.",
                "Both boots are lost under the bed.",
                "The boots are too big for puddles.",
                "The right boot has a hole.",
            ),
            question(
                "What happens when Tess tries to walk?",
                "Her toes are squeezed and she almost trips.",
                "She splashes all the way to school.",
                "The boots fall off in the grass.",
                "She finds a ball in a puddle.",
            ),
            question(
                "How does Tess fix the problem?",
                "She finds the right boot under the bench.",
                "She wears socks outside instead.",
                "She waits until the rain stops.",
                "She puts both left boots back on.",
            ),
        ],
    ),
    passage(
        "The Next Line",
        "Will",
        """
        Will's class was singing on the stage. Will knew the song, but when his line came, his mind went blank. He froze. The music kept going. His face felt hot, and he did not want to stop the whole song.

        His friend Hana hummed the first three notes, very softly. The notes were enough. Will remembered the words and sang them. His voice was shaky at first, then steady. The class sang the last line with him.

        People clapped. Will smiled at Hana and whispered thank you. He had not ruined the song. The next day he practiced that line two extra times so it would be ready.
        """,
        [
            question(
                "What is Will's problem on stage?",
                "He forgets the words to his line.",
                "The music stops before the song starts.",
                "Hana sings his line too loudly.",
                "The class does not know the song.",
            ),
            question(
                "How does Hana help?",
                "She hums the first three notes.",
                "She tells the class to sit down.",
                "She turns the music off.",
                "She sings the whole song alone.",
            ),
            question(
                "How does the story end?",
                "Will remembers the line and the class finishes.",
                "Will walks off the stage and hides behind the curtain.",
                "The song ends before his line.",
                "Hana forgets the notes too.",
            ),
        ],
    ),
    passage(
        "Jelly Side Down",
        "Cora",
        """
        Cora carried her sandwich to the table and tripped on the rug. The sandwich fell jelly side down. She reached to pick it up and eat it anyway. The jelly was full of fuzz from the rug.

        Dad said the floor was dirty, so the sandwich had to go in the trash. Cora frowned, but she threw it away. They washed their hands at the sink. Cora's stomach still growled.

        Dad got two slices of bread and the jelly jar. Cora spread the jelly, and Dad added the peanut butter. They cut the new sandwich in half. Cora ate it at the table, and this one stayed on the plate.
        """,
        [
            question(
                "What happens to Cora's sandwich?",
                "It falls jelly side down on the rug.",
                "Dad eats it before she sits down.",
                "The jelly jar is empty.",
                "It sticks to the ceiling.",
            ),
            question(
                "Why can't Cora eat the first sandwich?",
                "The rug made it dirty.",
                "She is not hungry anymore.",
                "Dad wants peanut butter instead.",
                "The plate is still in the sink.",
            ),
            question(
                "How is the problem solved?",
                "Cora and Dad make a new sandwich.",
                "Cora eats the fuzzy sandwich.",
                "They go out to buy lunch.",
                "Dad says she must skip lunch.",
            ),
        ],
    ),
    passage(
        "The Heavy Pack",
        "Dean",
        """
        Dean's backpack was so full that the strap hurt his shoulder. He had packed two trucks, a ball, and a box of blocks, plus his folder and book. On the walk to school he had to stop and rest. Mom asked what he needed for the day.

        Dean thought about it. He needed the folder and the book. He did not need the toys until he got home. He took the trucks, the ball, and the blocks out and set them by the door.

        The backpack felt light. Dean walked the rest of the way without stopping. His shoulder did not hurt. After school the toys were still by the door, ready for him to play.
        """,
        [
            question(
                "What is Dean's problem?",
                "His backpack is too heavy and the strap hurts.",
                "He forgot his folder at school.",
                "Mom will not walk with him.",
                "The toys do not fit in the space by the front door.",
            ),
            question(
                "What does Dean take out of the backpack?",
                "The trucks, the ball, and the blocks",
                "Only the folder and the reading book",
                "His lunch and his coat",
                "Nothing at all",
            ),
            question(
                "How does the story end?",
                "The light pack is easy to carry to school.",
                "Dean stays home because the strap hurts.",
                "He puts the toys back in and keeps walking.",
                "Mom carries the heavy pack for him.",
            ),
        ],
    ),
    passage(
        "Lights Out",
        "Hope",
        """
        Hope and Dad were playing a board game when the lights went out. A storm had knocked them off. The room was dark, and Hope could not see the pieces. She started to stand up fast. Dad said to sit still so nobody would trip.

        They waited. Dad felt his way to the kitchen drawer and got the flashlight. He clicked it on and set it so the beam lit the board. Hope could see her piece again. The rain tapped the window, but the game was bright.

        They finished the game by flashlight. Hope was not scared anymore. She helped Dad put the flashlight back in the drawer, right where they could find it the next time. Then they listened to the rain.
        """,
        [
            question(
                "What is the problem during the game?",
                "The lights go out and Hope cannot see the pieces.",
                "Dad loses the board under the couch.",
                "The flashlight will not fit in the drawer.",
                "Hope does not want to play anymore.",
            ),
            question(
                "Why does Dad tell Hope to sit still?",
                "So nobody will trip in the dark",
                "So she will win the game",
                "So the rain will stop",
                "So the lights will turn on",
            ),
            question(
                "How do they finish the game?",
                "Dad lights the board with a flashlight.",
                "They wait until morning to play.",
                "Hope plays without looking.",
                "They move the game outside.",
            ),
        ],
    ),
    passage(
        "The Shy Turtle",
        "Felix",
        """
        Felix brought his turtle, Skip, for show and tell. Skip stayed inside his shell. Felix tapped the shell lightly. Skip did not come out. Some students leaned in, and Skip pulled back even more.

        The teacher said to wait and be quiet. Felix set a small leaf by the shell and sat still. He did not tap again. The class got quiet too. They watched without crowding the table.

        Skip's head peeked out, then one foot. The class whispered. Felix smiled and told them Skip was shy, not sleepy. He let Skip eat the leaf. Show and tell worked because Felix had waited.
        """,
        [
            question(
                "What is Felix's problem at show and tell?",
                "Skip will not come out of his shell.",
                "Felix forgot to bring Skip to school.",
                "The leaf is too big for the table.",
                "The class is too quiet to hear him.",
            ),
            question(
                "What happens when students lean in?",
                "Skip pulls back even more.",
                "Skip crawls onto Felix's hand.",
                "The teacher ends show and tell.",
                "Felix taps the shell harder.",
            ),
            question(
                "What finally brings Skip out?",
                "Felix waits quietly and sets out a leaf.",
                "Felix taps the shell again and again.",
                "The class shouts Skip's name.",
                "Felix takes Skip back to his shell at home.",
            ),
        ],
    ),
]
