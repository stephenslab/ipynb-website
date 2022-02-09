alias jnbinder="mkdir -p .sos && docker run --rm -v $PWD:$PWD -v /tmp:/tmp -v $PWD/.sos:$PWD/.sos -t -w=$PWD -u 1000:1000 gaow/jnbinder jnbinder"
