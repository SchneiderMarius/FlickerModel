#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _izap_reg(void);
extern void _SinClamp_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," \"izap.mod\"");
    fprintf(stderr," \"SinClamp.mod\"");
    fprintf(stderr, "\n");
  }
  _izap_reg();
  _SinClamp_reg();
}
