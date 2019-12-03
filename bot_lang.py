__all__ = ('languages')

russian = {
    'start_1': 'Чтобы узнать больше о преобразованиях Фурье, используйте /about. \nЧтобы узнать поддерживаемые команды, используйте /commands. \nС помощью этого бота вы можете создавать увлекательные гифки, такие как эта:',
    'start_2': 'Отправьте мне картинку с чётко определенной текстурой и границами, желательно с однотонным фоном. Используйте /examples, чтобы просмотреть примеры изображений.',
    'commands': '/start - запустить Fourier Transform Bot \n/commands - вывести список поддерживаемых команд \n/language - изменить язык бота \n/about - показать информацию о преобразовании Фурье \n/examples - показать примеры обрабатываемых изображений \n/help - вывести справочную информацию \n',
    'language': 'Пожалуйста, выберите язык',
    'about': """
    Преобразование Фурье - это инструмент, который разбивает форму волны (функцию или сигнал) на альтернативное представление, характеризуемое синусом и косинусом. Преобразование Фурье показывает, что любой сигнал может быть переписан как сумма синусоидальных функций.
Преобразование Фурье - это способ для нас взять объединенную волну и вернуть обратно каждую синусоидальную волну.
Почему? Оказывается, многие вещи в реальном мире взаимодействуют на основе этих синусоидальных волн. Мы обычно называем их частотами волны.
Наиболее очевидным примером является звук - когда мы слышим звук, мы не слышим эту волнистую линию, но мы слышим различные частоты синусоидальных волн, из которых состоит звук.
Возможность разделить их на компьютере может дать нам понимание того, что человек на самом деле слышит. Мы можем понять, насколько высокий или низкий звук, или выяснить, что это за нота.
Мы также можем использовать этот процесс на волнах, которые не выглядят так, будто они сделаны из синусоидальных волн.
По сути, это то, что делают MP3, за исключением того, что они более умны в отношении того, какие частоты они сохраняют и какие они выбрасывают. В действительности у нас есть другой формат данных, называемый SVG, который, вероятно, лучше справляется с типами фигур, которые создаём мы. Итак, на данный момент, это действительно просто для того, чтобы делать увлекательные гифки.
    """,
    'photo_1': 'Загрузка...',
    'photo_2': 'Вас устраивает обработка изображения? \nПожалуйста, выберите наиболее подходящий из двух предложенных вариантов.',
    'text_1': 'Тогда начинаю преобразования.',
    'text_2': 'Отправьте более подходящее изображение.',
    'text_3': 'Всегда к вашим услугам!',
    'text_4': 'Мне обработать изображение с использованием глубокой сверточной нейронной сети для сегментации изображений?',
    'text_5': 'Начинаю обработку нейросетью. Это может занять несколько минут. Пожалуйста, подождите немного!',
    'other': 'Эта команда не распознана! Проверьте поддерживаемые команды /commands.',
    'error': 'Ошибка! \nГраница изображения не распознана! \nВозможно, оно является однотонным и не имеет границы. \nОтправьте мне картинку с чётко определенной текстурой и границами.'
}

english = {
    'start_1': 'To learn more about Fourier transforms click /about. \nTo see the commands supported click /commands. \nAnd now you can make mesmerizing things like this:',
    'start_2': 'Send me a photo with clearly defined texture and borders, preferably with a plain background. You can use /examples.',
    'commands': '/start - launch Fourier Transform Bot \n/commands - show list of supported commands \n/language - set bot language \n/about - show information about Fourier transforms \n/examples - show examples of images processed by the bot \n/help - show reference information \n',
    'language': 'Please choose the language.',
    'about': """
           The Fourier Transform is a tool that breaks a waveform (a function or signal) into an alternate representation characterized by sines and cosines. The Fourier Transform shows that any waveform can be re-written as the sum of sinusoidal functions.
The Fourier transform is a way for us to take the combined wave, and get each of the sine waves back out. 
Why? Turns out a lot of things in the real world interact based on these sine waves. We usually call them the wave's frequencies.
The most obvious example is sound – when we hear a sound, we don’t hear that squiggly line, but we hear the different frequencies of the sine waves that make up the sound.
Being able to split them up on a computer can give us an understanding of what a person actually hears. We can understand how high or low a sound is, or figure out what note it is.
We can also use this process on waves that don't look like they're made of sine waves.
This is essentially what MP3s do, except they're more clever about which frequencies they keep and which ones they throw away. In reality we have another data format called SVG, which probably does a better job for the types of shapes we tend to create. So for the moment, this is really just for making cool little gifs.
           """,
    'photo_1': 'Loading...',
    'photo_2': 'Are you satisfied with your image processed? \nPlease choose one of the two variants of the final picture.',
    'text_1': 'Then I start transforming the image.',
    'text_2': 'Download another more suitable image.',
    'text_3': 'Always at your service!',
    'text_4': 'Should I process the image using deep convolutional neural networks for image segmentation?',
    'text_5': "I'm starting neural network procession. It may take a few minutes. Please wait a bit!",
    'other': 'This command is not recognized! See supported /commands.',
    'error': 'Error! \nThe borders of the image can’t be defined. \nYou must’ve given me a plain background with nothing on it. \nPlease send me a photo with clearly defined texture and borders.'
}

deutsch = {
    'start_1': 'Um mehr über den Fourier-Transfirmationen zu erfahren, nutzen Sie /about. \nUm die unterstützte Befehle zu sehen, nutzen Sie /commands. \nJetzt können Sie spannende Bilder machen wie in diesem Beispiel:',
    'start_2': 'Schicken Sie mir ein fest umgrenztes Bild, am besten mit einem einfachen Hintergrund. Sie können auch /examples benutzen.',
    'commands': '/start - Fourier Transform Bot starten \n/commands - alle unterstützte Befehle zeigen \n/language - Sprache ändern \n/about - mehr Informationen über den Fourier-Transformationen zeigen \n/examples - Beispielbilder zeigen \n/help - Auskunft erteilen \n',
    'language': 'Wählen Sie bitte die Sprache aus.',
    'about': """
    Die Fourier-Transformation ist ein Zeug, das eine Wellenform (eine Funktion oder Signal) in eine alternative Darstellung zerbrecht, charakterisiert mit Sinuse und Kosinuse. Die Fourier-Transformation zeigt, dass jede Wellenform als eine Summe Sinusförmiger Funktionen neu geschrieben werden kann.
    Die Fourier-Transformation ist für uns die Art und Weise eine kombinierte Welle zu nehmen und jede Sinuswelle zurückbekommen.
    Warum? Es stellt sich heraus, dass viele Sachen in unserem Welt eufeinander mithilfe dieser Sinuswellen einwirken. Wir nennen sie gewöhnlich Wellenfrequenze.
    Das deutlichste Beispiel ist Laut: wenn wir das hören, sehen wir keine gewellte Kurve, aber wir hören verschiedene Frequenzen der Sinuswellen, die den Laut machen. Die Möglichkeit, sie am Computer zu teilen, gibt uns das Verstehen von was eine Person wirklich hört. Wir können verstehen, wie hoch oder niedrig der Laut ist, oder die Note erkennen.
    Wir können dieses Prozess auch für solchen Kurven benutzen, die nicht so aussehen, ais ob sie aus Sinuswellen gemacht sind.
    Das ist im Grunde genommen was MP3 machen, außer dass sie besser verstehen, welche Frequenze zu lassen und welche wegzuwerfen. In der Realität gibt es einen anderen Dataformat, das SVG heißt. SVG arbeitet wahrscheinlich besser mit den Figurenformen, die wir oft erschaffen. Also zum Moment ist das wirklich nur um schöne kleine gifs zu machen. 
    """,
    'photo_1': 'Ladung...',
    'photo_2': 'Passt Ihnen die Bearbeitung Ihres Bildes? \nWählen Sie bitte das Beste aus den zwei Ergebnissen.',
    'text_1': 'Dann fange ich mit der Transformation des Bildes an. Das könnte ein Paar minuten sein. Warten Sie bitte ein Bisschen ab!',
    'text_2': 'Schicken Sie bitte ein besser passendes Bild.',
    'text_3': 'Ich stehe zu Ihren Diensten!',
    'text_4': 'Soll ich jetzt anfangen mit der Bearbeitung durch Tieffaltungsneuronetzwerk',
    'text_5': 'Ich fange mit der Neuronetzwerkbearbeitung an. Das könnte ein Paar minuten sein. Warten Sie bitte ein Bisschen ab!',
    'other': 'Das Befehl ich nicht erkannt! Sehen Sie bitte /commands an.',
    'error': 'Fehler! \nDie Grenzen des Bildes sind nicht bestimmt! \nSie haben mir vielleicht nur den Eintonnenhintergrund gesendet. \nSchicken Sie mir ein fest umgrenztes Bild.'
}

languages = [russian, english, deutsch]