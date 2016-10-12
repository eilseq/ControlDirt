l = Liveness();

for (0, 5, {
    |index| l.addControl(\SimpleKnob, index, { arg addr, value; value.postln; })
});
