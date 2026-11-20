SL = {}

def slide(n, kicker, titulo, sub, fuente, body, narr, fotos=(), sig=()):
    SL[n] = dict(
        kicker=kicker,
        titulo=titulo,
        sub=sub,
        fuente=fuente,
        body=body,
        narr=narr.strip(),
        fotos=list(fotos),
        sig=list(sig),
    )
