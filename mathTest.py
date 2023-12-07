"""
Trying to find the model from speaker to microphone. There are several ways converting t-domain to frequency-domain
to find the model(z-domain can do it too, but I am not familiar with it :) ):

    1.omega-domain
    2.s-domain

By the control textbook, the first idea will be give a unit impulse to the speaker, and record the impulse response
from the microphone. Then, we can use the impulse response to find the model. However, the impulse response is not
easy to get. So, I will use the second idea giving a unit step to the speaker, and record the step response from the
microphone. Then, we can use the step response to find the model. The step response is easy to get.

Now, I have a target curve(Harman Curve which is seems to be a power spectrum) and a step response.
I want to find the model from the step response. Then add a filter to make the step response to close the target curve.
Finally, the filter would be added to the speaker to make the speaker to close the target curve.
1. omega-domain:
    How to find the model from the step response?

        unit step -> the model(speaker to microphone) -> step response -> fft -> frequency response

    Let set an ideal situation:

        X(unit step) ----> P(speaker) -----> Y(Target curve)

    however, the real situation is:

        X(unit step) ----> P(speaker) -----> Y'(frequency response)

    Now, we have the target curve and the frequency response. We want to find the model from the frequency response.
    Comparing the frequency response with the target curve, add a filter to make the frequency response to close the
    target curve.

        M(filter) = Y(Target curve) - Y'(frequency response)

    Now, we have the filter. We can add the filter to the speaker to make the speaker to close the target curve.

        X(unit step) ---->[Y(Target curve) - Y'(frequency response)] ----> P(speaker) -----> Y(Target curve)

    which is:

        X(unit step) ----> M(filter) ----> P(speaker) -----> Y(Target curve)

how to write the code?
The first priority is to get the M(filter). Then set M to the speaker. Finally, check the result.


2. s-domain:
    In this case, it'll be a little bit complicated, cause the filter setting usually is in omega-domain and the
    target curve is also in omega-domain. So, it may a bad idea to use s-domain. However, I still want to try it, if I
    have time.

    In Process

"""