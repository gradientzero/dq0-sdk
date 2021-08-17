echo "RUN SDK Demos"
echo "   --- CENSUS ---  "
echo "   ++ RUN Census raw ++  "
python ./dq0/examples/census/raw/run_demo.py

echo
echo "   ++ RUN Census raw with probability calibration ++  "
python ./dq0/examples/census/raw/run_demo_probas_calibration.py

echo
echo "   ++ RUN Census raw with metadata and preprocessor class ++  "
python ./dq0/examples/census/raw_meta_preprocessor/run_demo.py

echo
echo "   ++ RUN Census bayesian ++  "
python ./dq0/examples/census/bayesian/run_demo.py

echo
echo "   ++ RUN Census TUEV ++  "
python ./dq0/examples/census/TUEV/run_demo.py

echo
echo "   --- CIFAR ---  "
python ./dq0/examples/cifar/run_demo.py

echo
echo "   --- Human Acitivity Recognition ---  "
python ./dq0/examples/har/run_demo.py

echo
echo "   --- Medical Insurance ---  "
echo "   ++ RUN Medical Insurance default ++  "
python ./dq0/examples/medical_insurance/run_demo.py

echo
echo "   ++ RUN Medical Insurance with preprocessor ++  "
python ./dq0/examples/medical_insurance/demo_with_preprocessor/run_demo.py

echo
echo "   --- Newsgroups ---  "
echo "   ++ RUN Newsgroups bayesian ++  "
python ./dq0/examples/newsgroups/bayesian/run_demo.py

echo
echo "   ++ RUN Newsgroups network ++  "
python ./dq0/examples/newsgroups/network/run_demo.py

echo
echo "   --- Purchase-10 ---  "
python ./dq0/examples/purchase_10_600/nn/run_demo.py

echo
echo "   --- Purchase-100 ---  "
echo "   ++ RUN Purchase-100 bayesian ++  "
python ./dq0/examples/purchase_100_600/bayesian/run_demo.py

echo
echo "   ++ RUN Purchase-100 network ++  "
python ./dq0/examples/purchase_100_600/nn/run_demo.py