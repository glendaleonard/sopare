#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2015 - 2017 Martin Kauss (yo@bishoph.org)

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""

import pyaudio
import audioop
import math

class test_audio():

    SAMPLE_RATES = [ 8000, 11025, 12000, 16000, 22050, 32000, 44100, 48000 ]
    CHUNKS = [ 500, 1000, 2000, 4000, 8000 ]
    TEST_RESULTS = { }

    def __init__(self):
        print ("test_audio init...")
        self.good_sample_rates = [ ]
        self.good_chunks = [ ]
        self.silence = [ ]
        self.stream = None
        self.pa = pyaudio.PyAudio()
        print ('\n\n##### Default input device info #####')
        for k, v in self.pa.get_default_input_device_info().iteritems():
            print (str(k) + ': ' + str(v))
        print ('#####################################\n\n')

    def open(self, sample_rate, chunk):
        test_result = False
        try:
            self.stream = self.pa.open(format = pyaudio.paInt16,
                channels = 1,
                rate=sample_rate,
                input=True,
                output=False)
            test_result = True
        except IOError as e:
            test_result = False
            print ("Error: " + str(e))
        return test_result

    def read(self, chunks, loops):
        test_result = False
        vol = 0
        try:
            for x in range(loops):
                buf = self.stream.read(chunks)
                current_vol = audioop.rms(buf, 2)
                if (current_vol > vol):
                    vol = current_vol
            self.silence.append(vol)
            test_result = True
            print ('Excellent. Got all '+str(chunks*loops) + ' chunks.')
        except IOError as e:
            test_result = False
            print ("Error: "+ str(e))
        return test_result

    def test_sample_rates(self):
        print ('testing different SAMPLE_RATEs ... this may take a while!\n\n')
        for test_sample_rate in test_audio.SAMPLE_RATES:
            test_result = ta.open(test_sample_rate, test_sample_rate)
            if (test_result == True):
                self.good_sample_rates.append(test_sample_rate)
            if (self.stream != None):
                self.stream.close()

    def test_chunks(self):
        print ('testing different CHUNK sizes ... this may take a while!\n\n')
        for good_sample_rate in self.good_sample_rates:
            for chunks in test_audio.CHUNKS:
                test_result = ta.open(good_sample_rate, chunks)
                if (test_result == True):
                    if (good_sample_rate not in test_audio.TEST_RESULTS):
                        test_audio.TEST_RESULTS[good_sample_rate] = [ ]
                    read_test_result = ta.read(chunks, 10)
                    if (read_test_result == True):
                        self.good_chunks.append(chunks)
                        test_audio.TEST_RESULTS[good_sample_rate].append(chunks)
                        
                if (self.stream != None):
                    self.stream.close()

    def test_results(self):
        recommendations = { }
        found = False
        for sample_rate in test_audio.TEST_RESULTS:
            if (len(test_audio.TEST_RESULTS[sample_rate]) > 0):
                recommendations[sample_rate] = len(test_audio.TEST_RESULTS[sample_rate])
                found = True
        print ('\n\n')
        if (found == True):
            best = sorted(recommendations, key=recommendations.__getitem__, reverse=False)
            print ('Your sopare/config.py recommendations:\n')
            print ('SAMPLE_RATE = '+str(best[0]))
            print ('CHUNK = '+str(min(test_audio.TEST_RESULTS[best[0]])))
            treshold = int(math.ceil(max(self.silence) / 100.0)) * 100
            print ('THRESHOLD = '+str(treshold))
        else:
            print ('No recommendations, please fix your environment and try again!')

ta = test_audio()
ta.test_sample_rates()
ta.test_chunks()
ta.test_results()
